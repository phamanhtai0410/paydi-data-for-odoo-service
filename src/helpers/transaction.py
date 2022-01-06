
"""
   Description: 
        -
        -
"""

class TransactionHelper(object):
    @staticmethod
    def get_filter_by_obj_type(filter={}, obj_type=''):
        filter['obj_type'] = obj_type
        return filter
    
    @staticmethod
    def get_filter_card_type(filter={}, card_type=''):
        filter['obj_type'] = 'card'
        filter['extract.card_type'] = card_type