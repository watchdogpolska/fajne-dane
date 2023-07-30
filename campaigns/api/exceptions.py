from rest_framework.exceptions import APIException


class InstitutionGroupHasDocuments(APIException):
    status_code = 409
    default_detail = 'Documents with selected institution groups still exists.'
    default_code = 'institution_groups_has_documents'


class InstitutionHasDocuments(APIException):
    status_code = 409
    default_detail = 'Documents with selected institution still exists.'
    default_code = 'institution_has_documents'


class FileSourceNotProcess(APIException):
    status_code = 409
    default_detail = 'This file source was not processed yet.'
    default_code = 'file_source_not_processed'
