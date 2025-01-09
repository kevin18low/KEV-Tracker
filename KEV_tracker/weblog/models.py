from django.db import models


class EventLog(models.Model):
    status = models.CharField(db_column='Status', max_length=255)  # Field name made lowercase.
    time = models.CharField(db_column='Time', max_length=255)  # Field name made lowercase.
    newrecords = models.IntegerField(db_column='NewRecords')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Event_log'


class KevCatalog(models.Model):
    cveid = models.TextField(db_column='cveID', blank=True, null=True)  # Field name made lowercase.
    vendorproject = models.TextField(db_column='vendorProject', blank=True, null=True)  # Field name made lowercase.
    product = models.TextField(blank=True, null=True)
    vulnerabilityname = models.TextField(db_column='vulnerabilityName', blank=True, null=True)  # Field name made lowercase.
    dateadded = models.TextField(db_column='dateAdded', blank=True, null=True)  # Field name made lowercase.
    shortdescription = models.TextField(db_column='shortDescription', blank=True, null=True)  # Field name made lowercase.
    requiredaction = models.TextField(db_column='requiredAction', blank=True, null=True)  # Field name made lowercase.
    duedate = models.TextField(db_column='dueDate', blank=True, null=True)  # Field name made lowercase.
    knownransomwarecampaignuse = models.TextField(db_column='knownRansomwareCampaignUse', blank=True, null=True)  # Field name made lowercase.
    notes = models.TextField(blank=True, null=True)
    cwes = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'KEV_Catalog'