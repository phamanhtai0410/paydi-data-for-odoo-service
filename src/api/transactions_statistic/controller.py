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
# from src.decorators.response import handle_response
from src.exceptions import ExceptionNotFound

from bson import ObjectId
from flask import g, request

from src.decorators.request import load_data
from src.schemas.transactions_statistic import GetListTransactions, GetListErrorTransactionsResponse, GetListCardTransactionsResponse, GetListPreAuthTransactionsResponse, GetListTransactionsResponse
from src.utils.logger import Logger, LoggerTask
from src.services.transaction import TransactionService
from src.exceptions.missing import ExceptionMissing
from paydi_lib.decorators import auth_service, handle_response

@handle_response()
@auth_service()
def get_list_transactions():
    limit = request.args.get('limit', 10, type=int)
    offset = request.args.get('offset', 0, type=int)
    search_type = request.args.get('search_type', '', type=str)
    search_status = request.args.get('search_status', '', type=str)
    search_merchant = request.args.get('search_merchant', '', type=str)
    
    transactions, total = TransactionService.get_list_transactions(
        limit,
        offset,
        search_type,
        search_status,
        search_merchant
    )
    
    Logger.debug(f'List transactions <1> = {transactions}')
    
    if not isinstance(transactions, list):
        transactions = []


    return GetListTransactionsResponse.load_response({
        'transactions': transactions,
        'total': total
    })

@handle_response()
@auth_service()
def get_list_error_transactions():
    limit = request.args.get('limit', 10, type=int)
    offset = request.args.get('offset', 0, type=int)
    search_app_ver = request.args.get('search_app_ver', '', type=str)
    search_code = request.args.get('search_code', '', type=str)
    search_description = request.args.get('search_description', '', type=str)
    search_bank_code = request.args.get('search_bank_code', '', type=str)
    search_merchant = request.args.get('search_merchant', '', type=str)
    
    transactions, total = TransactionService.get_list_error_transactions(
        limit,
        offset,
        search_app_ver,
        search_code,
        search_description,
        search_bank_code,
        search_merchant
    )
    Logger.debug(f'List transactions <2> = {transactions}')
    if not isinstance(transactions, list):
        transactions = []


    return GetListErrorTransactionsResponse.load_response({
        'transactions': transactions,
        'total': total
    })

@handle_response()
@auth_service()
def get_list_card_transactions():
    limit = request.args.get('limit', 10, type=int)
    offset = request.args.get('offset', 0, type=int)
    search_batch_no = request.args.get('search_batch_no', '', type=str)
    search_app_ver = request.args.get('search_app_ver', '', type=str)
    search_code = request.args.get('search_code', '', type=str)
    search_description = request.args.get('search_description', '', type=str)
    search_tranx_type = request.args.get('search_tranx_type', '', type=str)
    search_bank_code = request.args.get('search_bank_code', '', type=str)
    search_merchant = request.args.get('search_merchant', '', type=str)
    
    transactions, total = TransactionService.get_list_card_transactions(
        limit, 
        offset,
        search_batch_no,
        search_app_ver,
        search_code,
        search_description,
        search_tranx_type,
        search_bank_code,
        search_merchant
    )

    if not isinstance(transactions, list):
        transactions = []


    return GetListCardTransactionsResponse.load_response({
        'transactions': transactions,
        'total': total
    })

@handle_response()
@auth_service()
def get_list_pre_auth_transactions():
    limit = request.args.get('limit', 10, type=int)
    offset = request.args.get('offset', 0, type=int)
    search_invoice_no = request.args.get('search_invoice', '', type=str)
    search_has_voided = request.args.get('search_has_voided', '', type=bool)
    search_bank_code = request.args.get('search_bank_code', '', type=str)
    search_merchant = request.args.get('search_merchant', '', type=str)
    
    transactions, total = TransactionService.get_list_pre_auth_transactions(
        limit, 
        offset, 
        search_invoice_no,
        search_bank_code,
        search_merchant
    )

    if not isinstance(transactions, list):
        transactions = []


    return GetListPreAuthTransactionsResponse.load_response({
        'transactions': transactions,
        'total': total
    })