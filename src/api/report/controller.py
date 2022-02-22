# -*- coding: utf-8 -*-



# File: controller.py
# Created at 16/11/2021
"""
   Description:
        -
        -
"""
from datetime import datetime
from json import load
from src.decorators.response import handle_response
from src.exceptions import ExceptionNotFound

from bson import ObjectId
from flask import g, request

from src.decorators.request import load_data
from src.schemas.report import *
from src.utils.logger import Logger, LoggerTask
from src.services.report import ReportService
from src.exceptions.missing import ExceptionMissing
from paydi_lib.decorators import auth_service

@handle_response()
@auth_service()
@load_data(GetListReport)
def get_list_reports_for_admin():
    limit = request.args.get('limit', 10, type=int)
    offset = request.args.get('offset', 0, type=int)
    reports, total = ReportService.get_list_report_for_admin(limit, offset)
    if not isinstance(reports, list):
        reports = []
    LoggerTask.debug(f'Get list reports for admin {reports}')
    return GetListReportsResponse.load_response({
        'reports': reports,
        'total': total
    })