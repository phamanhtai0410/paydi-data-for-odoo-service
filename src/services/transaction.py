# -*- coding: utf-8 -*-


# File: report.py	
# Created at 16/11/2021
"""
   Description: 
        -
        -
"""
from src.models.report import Report
from src.models.transaction import TransactionModel, ErrorTransactionModel, CardTransactionModel, PreAuthTransactionModel
from src.enums.transaction import TransactionStatusEnum, TransactionTopicKeyEnum
from src.utils.logger import LoggerTask, Logger

class TransactionService(object):
    @staticmethod
    def get_list_transactions(limit: int,
                              offset: int,
                              search_type: str,
                              search_status: str
                              ) -> list:
        filter = {}
        if search_status:
            filter['status'] = search_status
        if search_type:
            filter['obj_type'] = search_type

        Logger.debug(f'Filter = {filter}')
        
        transactions = TransactionModel.get_by_filter(
            filter=filter,
            options={
                'limit': limit,
                'offset': offset,
                'sort': {
                    'created_time': -1
                }
            }
        )
        
        if len(transactions) < limit:
            return transactions, offset + len(transactions)
        else:
            return transactions, offset + limit + limit // 2
    

    @staticmethod
    def get_list_error_transactions(limit: int,
                                    offset: int,
                                    search_app_ver: str,
                                    search_code: str,
                                    search_description: str,
                                    search_bank_code: str,
                                    ) -> list:
        filter = {}
        if search_app_ver:
            filter['app_ver'] = {
                '$regex': search_app_ver
            }
        if search_code:
            filter['code'] = {
                '$regex': search_code
            }
        if search_description:
            filter['desc'] = {
                '$regex': search_description
            }
        if search_bank_code:
            filter['bank_code'] = {
                '$regex': search_bank_code
            }
            
        Logger.debug(f'Filter = {filter}')
        transactions = ErrorTransactionModel.get_by_filter(
            filter=filter,
            options={
                'limit': limit,
                'offset': offset,
                'sort': {
                    'created_time': -1
                }
            }
        )
        if len(transactions) < limit:
            return transactions, offset + len(transactions)
        else:
            return transactions, offset + limit + limit // 2

    @staticmethod
    def get_list_card_transactions(limit: int,
                                   offset: int,
                                   search_batch_no: str,
                                   search_app_ver: str,
                                   search_code: str,
                                   search_description: str,
                                   search_tranx_type: str,
                                   search_bank_code: str,
                                   ) -> list:
        filter = {}
        if search_batch_no:
            filter['batch_no'] = {
                "$regex": search_batch_no
            }
        if search_app_ver:
            filter['app_ver'] = {
                "$regex": search_app_ver
            }
        if search_code:
            filter['code'] = {
                "$regex": search_code
            }
        if search_description:
            filter['desc'] = {
                "$regex": search_description
            }
        if search_tranx_type:
            filter['tranx_type'] = {
                "$regex": search_tranx_type
            }
        if search_bank_code:
            filter['bank_code'] = {
                '$regex': search_bank_code
            }
        
        Logger.debug(f'Filter = {filter}')
        transactions = CardTransactionModel.get_by_filter(
            filter=filter,
            options={
                'limit': limit,
                'offset': offset,
                'sort': {
                    'created_time': -1
                }
            }
        )
        if len(transactions) < limit:
            return transactions, offset + len(transactions)
        else:
            return transactions, offset + limit + limit // 2

    @staticmethod
    def get_list_pre_auth_transactions(limit: int,
                                       offset: int,
                                       search_invoice_no: str,
                                       search_bank_code: str,
                                       ) -> list:
        filter = {}
        if search_invoice_no:
            filter['invoice_no'] = {
                "$regex": search_invoice_no
            }
        if search_bank_code:
            filter['bank_code'] = {
                '$regex': search_bank_code
            }
        
        transactions = PreAuthTransactionModel.get_by_filter(
            filter=filter,
            options={
                'limit': limit,
                'offset': offset,
                'sort': {
                    'created_time': -1
                }
            }
        )
        if len(transactions) < limit:
            return transactions, offset + len(transactions)
        else:
            return transactions, offset + limit + limit // 2

