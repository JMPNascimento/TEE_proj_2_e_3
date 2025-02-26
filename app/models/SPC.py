import numpy as np
import json
import random
import requests

TELEGRAM_BOT_TOKEN = "7821098978:AAHKYlf0sLitACMKGNmsp2-uJn1v0kV2PPg"
TELEGRAM_CHAT_ID = "YOUR_ID" # Search for userinfobot on Telegram to get your User ID

def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    data = {"chat_id": TELEGRAM_CHAT_ID, "text": message}
    requests.post(url, data=data)

class ControlChart:
    def __init__(self, num_samples=10, sample_size=5, loc=10, scale=3, outlier_prob=0.3):
        self.num_samples = num_samples
        self.sample_size = sample_size
        self.loc = loc
        self.scale = scale
        self.outlier_prob = outlier_prob
        self.global_data = []
        self.sample_results = []
        self.outliers_per_sample = []
        self.control_limits = {}
        self.individual_values = []
        self.moving_ranges = []
        self.notificar = True

    def toggle_notifications(self):
        self.notificar = not self.notificar
        status = "ativadas" if self.notificar else "desativadas"
        print(f"Notificações {status}")
        return {"message": f"Notificações {status}", "status": self.notificar}
    
    def generate_data(self):
        self.global_data = [
            list(map(float, np.round(np.random.normal(loc=self.loc, scale=self.scale, size=self.sample_size), 2)))
            for _ in range(self.num_samples)
        ]

        json_data = json.dumps({"data": self.global_data})
        return json_data 

    def update_data(self, new_data):
        print(f"Received new_data: {new_data}")
        if not isinstance(new_data, list) or not all(isinstance(value, (int, float)) for value in new_data):
            raise ValueError("new_data must be a list of numbers.")
        
        new_data = np.array(new_data).reshape(-1, self.sample_size)

        if not hasattr(self, "global_data") or len(self.global_data) == 0:
            self.global_data = new_data
        else:
            self.global_data = np.vstack((self.global_data, new_data))

        print(f"🔄 Dados armazenados atualizados: {self.global_data.shape}")

        self.sample_results = []
        self.outliers_per_sample = []
        self.individual_values = []
        self.moving_ranges = []
        self.control_limits = {}

        self.calculate_statistics()

        if self.notificar:
            self.check_for_outliers_and_notify()

    def calculate_statistics(self):
        for sample_set in self.global_data:
            ls = np.array(sample_set)
            q1 = np.percentile(ls, 25)
            q3 = np.percentile(ls, 75)
            iqr = q3 - q1

            lower_limit = q1 - 1.5 * iqr
            upper_limit = q3 + 1.5 * iqr

            outliers = ls[(ls < lower_limit) | (ls > upper_limit)]
            treated_data = ls[(ls >= lower_limit) & (ls <= upper_limit)]

            if len(treated_data) < 2:
                treated_data = ls

            if len(outliers) < 2:
                outliers = []

            mean = np.mean(treated_data)
            amplitude = np.max(treated_data) - np.min(treated_data)
            std = np.std(treated_data, ddof=1) if len(treated_data) > 1 else 0
            samp_outliers = np.mean(outliers) if len(outliers) > 0 else None

            self.sample_results.append([mean, amplitude, std, samp_outliers])
            self.outliers_per_sample.append(outliers)

        self.calculate_individual_values()
        self.calculate_moving_range_values()
        self._calculate_control_limits()
            

    def calculate_individual_values(self):
        self.individual_values = np.concatenate(self.global_data)

    def calculate_moving_range_values(self):
        if self.individual_values is None or len(self.individual_values) < 2:
            self.moving_ranges = []
        else:
            self.moving_ranges = np.abs(np.diff(self.individual_values))
        return self.moving_ranges

    def _calculate_control_limits(self):
        global_mean = [res[0] for res in self.sample_results]
        global_amplitude = [res[1] for res in self.sample_results]
        global_std = [res[2] for res in self.sample_results]

        a2 = 0.577
        d3, d4 = 0.0, 2.114
        c4 = 0.940

        cl_X = np.mean(global_mean)
        cl_R = np.mean(global_amplitude)
        cl_s = np.mean(global_std)

        ucl_X = cl_X + a2 * cl_R
        ucl_R = d4 * cl_R
        ucl_s = cl_s + 3 * (cl_s / c4) * np.sqrt(1 - c4**2)

        lcl_X = cl_X - a2 * cl_R
        lcl_R = d3 * cl_R
        lcl_s = cl_s - 3 * (cl_s / c4) * np.sqrt(1 - c4**2)

        # self.moving_ranges = self.calculate_moving_range_values()
        
        if len(self.moving_ranges) == 0:
            cl_MR = 0
        else:
            cl_MR = np.mean(self.moving_ranges)

        d2 = 1.128
        ucl_MR = cl_MR * d2
        lcl_MR = 0 

        self.control_limits = {
            "cl_X": cl_X, "ucl_X": ucl_X, "lcl_X": lcl_X,
            "cl_R": cl_R, "ucl_R": ucl_R, "lcl_R": lcl_R,
            "cl_s": cl_s, "ucl_s": ucl_s, "lcl_s": lcl_s,
            "cl_MR": cl_MR, "ucl_MR": ucl_MR, "lcl_MR": lcl_MR,
            "global_mean": global_mean, "global_amplitude": global_amplitude, "global_std": global_std,
        }

    def check_for_outliers_and_notify(self):

        sample_set = self.global_data[-1]
        mean_value = np.mean(sample_set)
        amplitude_value = np.max(sample_set) - np.min(sample_set)
        std_value = np.std(sample_set, ddof=1)

        if mean_value > self.control_limits["ucl_X"] or mean_value < self.control_limits["lcl_X"]:
            message = f"ALERTA: Novo dado de média ({mean_value}) ultrapassou os limites de controle!"
            send_telegram_message(message)

        if amplitude_value > self.control_limits["ucl_R"] or amplitude_value < self.control_limits["lcl_R"]:
            message = f"ALERTA: Novo dado de amplitude ({amplitude_value}) ultrapassou os limites de controle!"
            send_telegram_message(message)

        if std_value > self.control_limits["ucl_s"] or std_value < self.control_limits["lcl_s"]:
            message = f"ALERTA: Novo dado de desvio padrão ({std_value}) ultrapassou os limites de controle!"
            send_telegram_message(message)
