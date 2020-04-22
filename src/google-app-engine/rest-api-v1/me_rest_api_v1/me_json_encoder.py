#!/usr/bin/env python3
"""
    me_rest_api_v1 - me_json_encoder.py

    JSON encoder for the Me-application
"""
#---------------------------------------------------------------------------------------------------
# Imports
from database import Database
from json import JSONEncoder
import datetime
#---------------------------------------------------------------------------------------------------
class MeJSONEncoder(JSONEncoder):
    """ JSON encoder for my own created classes """

    @staticmethod
    def convert_to_sa_dict(obj):
        """ Method to convert a SQLalchemy to a Python dict """

        # Get the fields that we should hide
        try:
            fields_to_hide = obj.api_hide_fields
        except AttributeError:
            fields_to_hide = list()

        # Get the columns
        columns = [ column.name for column in type(obj).__table__.columns ]

        # Then we create a dict with the only the column items
        column_dict = { key: value for key, value in obj.__dict__.items() if key in columns and not key in fields_to_hide }

        # Add fields that are in the 'api_extra_fields' list
        try:
            api_extra_fields = obj.api_extra_fields
        except AttributeError:
            api_extra_fields = list()
        
        # Loop through the extra fields and add them to the outgoing dict
        for extra_field in api_extra_fields:
            try:
                column_dict[extra_field] = obj.__getattribute__(extra_field)
            except AttributeError:
                column_dict[extra_field] = None

        # Check if a '__objectname__' is given and add it to the outgoing dict
        column_dict['_type'] = ''
        if '__objecttype__' in obj.__dir__():
            column_dict['_type'] = obj.__objecttype__

        # And we return that dict
        return column_dict

    def default(self, obj):
        """ Gets the object and encodes it in a way JSON can work with """

        # Serializer for database objects
        if isinstance(obj, Database.base_class):
            # Return the dict for the SQLalchemy object
            return MeJSONEncoder.convert_to_sa_dict(obj)
        # Serializer for datetime objects
        elif isinstance(obj, datetime.datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        else:
            raise TypeError(
                'Unserializable object "{}" of type "{}"'.format(obj, type(obj))
            )
#---------------------------------------------------------------------------------------------------