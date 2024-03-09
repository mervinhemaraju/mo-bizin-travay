# from pynamodb.indexes import GlobalSecondaryIndex, AllProjection
# from pynamodb.attributes import UnicodeAttribute


# class RecruiterIndex(GlobalSecondaryIndex):
#     """
#     This class represents a global secondary index
#     """

#     class Meta:
#         # index_name is optional, but can be provided to override the default name
#         index_name = "recruiter_index"
#         read_capacity_units = 2
#         write_capacity_units = 1
#         # All attributes are projected
#         projection = AllProjection()

#     # This attribute is the hash key for the index
#     # Note that this attribute must also exist
#     # in the model
#     recruiter = UnicodeAttribute()
