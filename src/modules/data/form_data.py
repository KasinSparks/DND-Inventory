from flask import request

def get_request_field_data(field_name):
    return request.form[field_name]

def convert_form_field_data_to_int(field_name):
    field_data = get_request_field_data(field_name)
    return 0 if field_data is None or field_data == '' else int(field_data)
