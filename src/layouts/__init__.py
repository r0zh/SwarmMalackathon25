"""
Layout modules for different dashboard sections
"""

from .header import create_header, create_footer
from .main_metrics import create_main_metrics
from .diagnostics import create_diagnostics_section
from .gender_analysis import create_gender_analysis_section
from .severity import create_severity_section
from .weight_stay import create_weight_stay_section
from .insights import create_insights_section

__all__ = [
    "create_header",
    "create_footer",
    "create_main_metrics",
    "create_diagnostics_section",
    "create_gender_analysis_section",
    "create_severity_section",
    "create_weight_stay_section",
    "create_insights_section",
]
