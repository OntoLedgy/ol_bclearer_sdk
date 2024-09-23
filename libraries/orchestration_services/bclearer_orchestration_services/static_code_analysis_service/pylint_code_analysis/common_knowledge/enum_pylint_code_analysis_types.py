from enum import unique, auto

from nf_common.code.services.static_code_analysis_service.common_knowledge.enum_code_analysis_types import \
    EnumCodeAnalysisTypes


@unique
class EnumPylintCodeAnalysisTypes(
        EnumCodeAnalysisTypes):
    REPORT = \
        auto()
