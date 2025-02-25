import numpy as np
import matplotlib.pyplot as plt
import io

from abc import ABC, abstractmethod

from .SPC import ControlChart

class BaseChartRenderer(ABC):
    def __init__(self, control_chart):
        self.control_chart = control_chart

    @abstractmethod
    def render(self):
        pass

    def _save_chart_to_buffer(self, fig):        
        buffer = io.BytesIO()
        fig.savefig(buffer, format='png')
        plt.close(fig)
        buffer.seek(0)
        return buffer

class XChartRenderer(BaseChartRenderer):
    def render(self):
        limits = self.control_chart.control_limits
        global_mean = limits["global_mean"]

        y_min = min(min(global_mean), limits["lcl_X"]) - 5
        y_max = max(max(global_mean), limits["ucl_X"]) + 5

        fig, ax = plt.subplots(figsize=(10, 6))
        ax.plot(global_mean, marker='o', label='Samples mean')
        ax.axhline(limits["cl_X"], color='green', linestyle='--', label='Central Line')
        ax.axhline(limits["ucl_X"], color='red', linestyle='--', label='UCL')
        ax.axhline(limits["lcl_X"], color='red', linestyle='--', label='LCL')
        ax.set_ylim(y_min, y_max)

        ax.set_title('Control Chart - X')
        ax.legend()
        ax.grid(True)

        return self._save_chart_to_buffer(fig)
    
class RChartRenderer(BaseChartRenderer):
    def render(self):
        limits = self.control_chart.control_limits
        global_amplitude = limits["global_amplitude"]

        fig, ax = plt.subplots(figsize=(10, 6))
        ax.plot(global_amplitude, marker='o', color='orange', label='Samples amplitude')
        ax.axhline(limits["cl_R"], color='green', linestyle='--', label='Central Line')
        ax.axhline(limits["ucl_R"], color='red', linestyle='--', label='UCL')
        ax.axhline(limits["lcl_R"], color='red', linestyle='--', label='LCL')

        ax.set_title('Control Chart - Amplitude (R)')
        ax.legend()
        ax.grid(True)

        return self._save_chart_to_buffer(fig)

class sChartRenderer(BaseChartRenderer):
    def render(self):
        limits = self.control_chart.control_limits
        global_std = limits["global_std"]

        fig, ax = plt.subplots(figsize=(10, 6))
        ax.plot(global_std, marker='o', color='purple', label='Samples standard deviation')
        ax.axhline(limits["cl_s"], color='green', linestyle='--', label='Central Line')
        ax.axhline(limits["ucl_s"], color='red', linestyle='--', label='UCL')
        ax.axhline(limits["lcl_s"], color='red', linestyle='--', label='LCL')

        ax.set_title('Control Chart - Standard Deviation (s)')
        ax.legend()
        ax.grid(True)

        return self._save_chart_to_buffer(fig)
    
class IndividualChartRenderer(BaseChartRenderer):
    def render(self):
        limits = self.control_chart.control_limits
        individual_values = self.control_chart.individual_values

        fig, ax = plt.subplots(figsize=(10, 6))
        ax.plot(individual_values, marker='o', label='Individual Values')
        ax.axhline(limits["cl_X"], color='green', linestyle='--', label='Central Line')
        ax.axhline(limits["ucl_X"], color='red', linestyle='--', label='UCL')
        ax.axhline(limits["lcl_X"], color='red', linestyle='--', label='LCL')

        ax.set_title('Control Chart - Individual (I)')
        ax.legend()
        ax.grid(True)

        return self._save_chart_to_buffer(fig)

class MovingRangeChartRenderer(BaseChartRenderer):
    def render(self):
        limits = self.control_chart.control_limits
        moving_ranges = self.control_chart.moving_ranges

        fig, ax = plt.subplots(figsize=(10, 6))
        ax.plot(moving_ranges, marker='o', label='Moving Ranges')
        ax.axhline(limits["cl_MR"], color='green', linestyle='--', label='Central Line')
        ax.axhline(limits["ucl_MR"], color='red', linestyle='--', label='UCL')
        ax.axhline(limits["lcl_MR"], color='red', linestyle='--', label='LCL')

        ax.set_title('Control Chart - Moving Range (MR)')
        ax.legend()
        ax.grid(True)

        return self._save_chart_to_buffer(fig)