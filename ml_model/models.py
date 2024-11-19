from django.db import models


class Vessel(models.Model):
    name = models.CharField(max_length=100)
    service = models.CharField(max_length=4, default=None, blank=True, null=True)
    previous_service = models.CharField(max_length=4, default=None, blank=True, null=True)

    def __str__(self):
        return f"Name: {self.name}, Service: {self.service}"
    



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
    voyage_complete = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.service} - {self.vessel} - {self.voyage_s}"



class BES(models.Model):
    week_etb_cgp = models.CharField(max_length=10, verbose_name='Wk/ETB CGP')
    service = models.CharField(max_length=10)
    vessel = models.CharField(max_length=100)
    voyage_s = models.CharField(max_length=10, verbose_name='Voyage-S')
    
    # Date fields for ETA, ETB, and ETD
    eta_cgp = models.DateField(verbose_name='ETA CGP')
    etb_cgp = models.DateField(verbose_name='ETB CGP')
    etd_cgp = models.DateField(verbose_name='ETD CGP')

    voyage_n = models.CharField(max_length=10, verbose_name='Voyage-N')

    eta_sin = models.DateField(verbose_name='ETA SIN')
    etb_sin = models.DateField(verbose_name='ETB SIN')
    etd_sin = models.DateField(verbose_name='ETD SIN')

    eta_pkg = models.DateField(verbose_name='ETA PKG')
    etb_pkg = models.DateField(verbose_name='ETB PKG')
    etd_pkg = models.DateField(verbose_name='ETD PKG')
    
    eta_cgp_2 = models.DateField(verbose_name='ETA CGP-2')
    etb_cgp_2 = models.DateField(verbose_name='ETB CGP-2')
    etd_cgp_2 = models.DateField(verbose_name='ETD CGP-2')
    voyage_complete = models.BooleanField(default=False)

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



class CCE_RV(models.Model):
    eta_to_etb_cgp = models.IntegerField(default=1,blank=True, null=True)
    etb_to_etd_cgp = models.IntegerField(default=2,blank=True, null=True)
    cgp_to_cmb = models.IntegerField(default=5,blank=True, null=True)
    eta_to_etb_cmb = models.IntegerField(default=1,blank=True, null=True)
    etb_to_etd_cmb = models.IntegerField(default=2,blank=True, null=True)
    cmb_to_cgp = models.IntegerField(default=5,blank=True, null=True)

    def __str__(self):
        return f"ETA to ETB CGP: {self.eta_to_etb_cgp}, ETB to ETD CGP: {self.etb_to_etd_cgp}, CGP to CMB: {self.cgp_to_cmb}, ETA to ETB CMB: {self.eta_to_etb_cmb}, ETB to ETD CMB: {self.etb_to_etd_cmb}, CMB to CGP: {self.cmb_to_cgp}"
    




class BES_RV(models.Model):
    eta_to_etb_cgp = models.IntegerField(default=1,blank=True, null=True)
    etb_to_etd_cgp = models.IntegerField(default=2,blank=True, null=True)
    cgp_to_sin = models.IntegerField(default=5,blank=True, null=True)
    eta_to_etb_sin = models.IntegerField(default=1,blank=True, null=True)
    etb_to_etd_sin = models.IntegerField(default=2,blank=True, null=True)
    sin_to_pkg = models.IntegerField(default=5,blank=True, null=True)
    eta_to_etb_pkg = models.IntegerField(default=1,blank=True, null=True)
    etb_to_etd_pkg = models.IntegerField(default=2,blank=True, null=True)
    pkg_to_cgp = models.IntegerField(default=5,blank=True, null=True)

    def __str__(self):
        return f"ETA to ETB CGP: {self.eta_to_etb_cgp}, ETB to ETD CGP: {self.etb_to_etd_cgp}, CGP to SIN: {self.cgp_to_sin}, ETA to ETB SIN: {self.eta_to_etb_sin}, ETB to ETD SIN: {self.etb_to_etd_sin}, SIN to PKG: {self.sin_to_pkg}, ETA to ETB PKG: {self.eta_to_etb_pkg}, ETB to ETD PKG: {self.etb_to_etd_pkg}, PKG to CGP: {self.pkg_to_cgp}"
    





class BES_Predicted(models.Model):
    week_etb_cgp = models.CharField(max_length=10, verbose_name='Wk/ETB CGP')
    service = models.CharField(max_length=10)
    vessel = models.CharField(max_length=100)
    voyage_s = models.CharField(max_length=10, verbose_name='Voyage-S')
    
    # Date fields for ETA, ETB, and ETD
    eta_cgp = models.DateField(verbose_name='ETA CGP')
    etb_cgp = models.DateField(verbose_name='ETB CGP')
    etd_cgp = models.DateField(verbose_name='ETD CGP')

    voyage_n = models.CharField(max_length=10, verbose_name='Voyage-N')

    eta_sin = models.DateField(verbose_name='ETA SIN')
    etb_sin = models.DateField(verbose_name='ETB SIN')
    etd_sin = models.DateField(verbose_name='ETD SIN')

    eta_pkg = models.DateField(verbose_name='ETA PKG')
    etb_pkg = models.DateField(verbose_name='ETB PKG')
    etd_pkg = models.DateField(verbose_name='ETD PKG')
    
    eta_cgp_2 = models.DateField(verbose_name='ETA CGP-2')
    etb_cgp_2 = models.DateField(verbose_name='ETB CGP-2')
    etd_cgp_2 = models.DateField(verbose_name='ETD CGP-2')

    def __str__(self):
        return f"{self.service} - {self.vessel} - {self.voyage_s}"


    







