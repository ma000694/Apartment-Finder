# this file holds all the service functions, checking and upholding logic, then calling the repository functions

import postgreSQL.property_repository as repo
from .property_data_class import Property

#TODO: ERROR AND RULE CHECKS

def list_properties():
    return repo.get_all_properties()

def fetch_property(id):
    return repo.fetch_property_from_id(id)

def fetch_properties(id_list):
    return repo.fetch_property_from_id(id_list)

def insert_property(property: Property):
    """
    inserts property using the custom Property data class
    returns new id of inserted property
    """
    return repo.insert_property(property)