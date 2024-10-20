from django.db import models


class Vessel(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=20)

    def __str__(self):
        return self.name
    



class Schedule(models.Model):
    week_etb_cgp = models.CharField(max_length=10, verbose_name='Wk/ETB CGP')
    service = models.CharField(max_length=10)
    vessel = models.CharField(max_length=100)
    voyage_s = models.CharField(max_length=10, verbose_name='Voyage-S')
    
    # Date fields for ETA, ETB, and ETD
    eta_cgp = models.DateField(verbose_name='ETA CGP')
    etb_cgp = models.DateField(verbose_name='ETB CGP')
    etd_cgp = models.DateField(verbose_name='ETD CGP')

    voyage_n = models.CharField(max_length=10, verbose_name='Voyage-N')
    
    eta_cmb = models.DateField(verbose_name='ETA CMB')
    etb_cmb = models.DateField(verbose_name='ETB CMB')
    etd_cmb = models.DateField(verbose_name='ETD CMB')
    
    eta_cgp_2 = models.DateField(verbose_name='ETA CGP-2')
    etb_cgp_2 = models.DateField(verbose_name='ETB CGP-2')
    etd_cgp_2 = models.DateField(verbose_name='ETD CGP-2')

    def __str__(self):
        return f"{self.service} - {self.vessel} - {self.voyage_s}"





class Predicted_Schedule(models.Model):
    week_etb_cgp = models.CharField(max_length=10, verbose_name='Wk/ETB CGP')
    service = models.CharField(max_length=10)
    vessel = models.CharField(max_length=100)
    voyage_s = models.CharField(max_length=10, verbose_name='Voyage-S')
    
    # Date fields for ETA, ETB, and ETD
    eta_cgp = models.DateField(verbose_name='ETA CGP')
    etb_cgp = models.DateField(verbose_name='ETB CGP')
    etd_cgp = models.DateField(verbose_name='ETD CGP')

    voyage_n = models.CharField(max_length=10, verbose_name='Voyage-N')
    
    eta_cmb = models.DateField(verbose_name='ETA CMB')
    etb_cmb = models.DateField(verbose_name='ETB CMB')
    etd_cmb = models.DateField(verbose_name='ETD CMB')
    
    eta_cgp_2 = models.DateField(verbose_name='ETA CGP-2')
    etb_cgp_2 = models.DateField(verbose_name='ETB CGP-2')
    etd_cgp_2 = models.DateField(verbose_name='ETD CGP-2')

    def __str__(self):
        return f"{self.service} - {self.vessel} - {self.voyage_s}"



class Analytics(models.Model):
    week_etb_cgp = models.CharField(max_length=10)
    service = models.CharField(max_length=10)
    vessel = models.CharField(max_length=100)
    voyage_s = models.CharField(max_length=10)
    eta_cgp = models.DateField()
    etb_cgp = models.DateField()
    diff_eta_etb_cgp = models.IntegerField(blank=True, null=True)
    etd_cgp = models.DateField()
    diff_etb_etd_cgp = models.IntegerField(blank=True, null=True)
    voyage_n = models.CharField(max_length=10)
    eta_cmb = models.DateField()
    diff_cgp_cmb = models.IntegerField(blank=True, null=True)
    etb_cmb = models.DateField()
    diff_eta_etb_cmb = models.IntegerField(blank=True, null=True)
    etd_cmb = models.DateField()
    diff_etb_etd_cmb = models.IntegerField(blank=True, null=True)
    eta_cgp_2 = models.DateField()
    etb_cgp_2 = models.DateField()
    etd_cgp_2 = models.DateField()

    class Meta:
        managed = False
        db_table = 'analytics'
    def __str__(self):
        return f"{self.service} - {self.vessel} - {self.voyage_s}"



class Item(models.Model):
    name = models.CharField(max_length=100)
    quantity = models.IntegerField()

    def __str__(self):
        return self.name



