from calendar import week
from datetime import datetime, timezone
import operator
from sre_constants import AT_END
from django.db import models



def get_berthing_delay(eta, atb):
    if eta and atb :
        eta_as_datetime = datetime.combine(eta, datetime.min.time()).replace(tzinfo=timezone.utc)

        time_diff = atb - eta_as_datetime
            # Calculate hours and minutes
        total_minutes = int(time_diff.total_seconds() / 60)
        hours = total_minutes // 60
        print(hours)
        minutes = total_minutes % 60
        print(minutes)
            # Store the difference in "HH:MM" format
        return f"{hours}h:{minutes}m"

    return None

class Vessel(models.Model):
    name = models.CharField(max_length=100)
    operator= models.CharField(max_length=100, blank=True, null=True)
    service = models.CharField(max_length=4, default=None, blank=True, null=True)
    previous_service = models.CharField(max_length=4, default=None, blank=True, null=True)

    def __str__(self):
        return f"Name: {self.name}, Service: {self.service}"
    



class Schedule(models.Model):
    week_etb_cgp = models.CharField(max_length=10, verbose_name='Wk/ETB CGP')
    operator = models.CharField(max_length=100, blank=True, null=True)
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
    operator = models.CharField(max_length=100, blank=True, null=True)
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
    






class BES_Complete(models.Model):

    operator = models.CharField(max_length=100,blank=True, null=True)
    service = models.CharField(max_length=10,blank=True, null=True)
    rv1 = models.IntegerField(blank=True, null=True)
    sb_v1 = models.IntegerField(blank=True, null=True)
    nb_v1 = models.IntegerField(blank=True, null=True)
    rv2 = models.IntegerField(blank=True, null=True)
    sb_v2 = models.IntegerField(blank=True, null=True)
    nb_v2 = models.IntegerField(blank=True, null=True)
    rv3 = models.IntegerField(blank=True, null=True)
    sb_v3 = models.IntegerField(blank=True, null=True)
    nb_v3 = models.IntegerField(blank=True, null=True)

    week_cgp = models.CharField(max_length=10, verbose_name='Week CGP',blank=True, null=True)
    only_vessel_name = models.CharField(max_length=100,blank=True, null=True)
    vessel_code = models.CharField(max_length=20,blank=True, null=True)
    vessel = models.CharField(max_length=100,blank=True, null=True)
    voyage_s = models.CharField(max_length=10, verbose_name='Voyage-S',blank=True, null=True)
    voyage_s_with_code = models.CharField(max_length=20, verbose_name='Voyage-S with Code',blank=True, null=True)
    terminal_cgp = models.CharField(max_length=100,blank=True, null=True) 
    # Date fields for ETA, ETB, and ETD
    eta_cgp = models.DateField(verbose_name='ETA CGP',blank=True, null=True)
    ata_cgp = models.DateTimeField(verbose_name='ATA CGP',blank=True, null=True)
    etb_cgp = models.DateField(verbose_name='ETB CGP',blank=True, null=True)
    atb_cgp = models.DateTimeField(verbose_name='ATB CGP',blank=True, null=True)
    etd_cgp = models.DateField(verbose_name='ETD CGP',blank=True, null=True)
    atd_cgp = models.DateTimeField(verbose_name='ATD CGP',blank=True, null=True)
    berthing_delay_cgp = models.CharField(max_length=15,blank=True, null=True)

 
    week_sin = models.CharField(max_length=10, verbose_name='Week SIN',blank=True, null=True)
    voyage_n = models.CharField(max_length=10, verbose_name='Voyage-N',blank=True, null=True)   
    voyage_n_with_code = models.CharField(max_length=20, verbose_name='Voyage-N with Code',blank=True, null=True)

    terminal_sin = models.CharField(max_length=100,blank=True, null=True)

    eta_sin = models.DateField(verbose_name='ETA SIN',blank=True, null=True)
    ata_sin = models.DateTimeField(verbose_name='ATA SIN',blank=True, null=True)
    etb_sin = models.DateField(verbose_name='ETB SIN',blank=True, null=True)
    atb_sin = models.DateTimeField(verbose_name='ATA SIN',blank=True, null=True)
    etd_sin = models.DateField(verbose_name='ETD SIN',blank=True, null=True)
    atd_sin = models.DateTimeField(verbose_name='ATD SIN',blank=True, null=True)
    berthing_delay_sin = models.CharField(max_length=15,blank=True, null=True)

    week_pkg = models.CharField(max_length=10, verbose_name='Week PKG',blank=True, null=True)
    terminal_pkg = models.CharField(max_length=100,blank=True, null=True)

    eta_pkg = models.DateField(verbose_name='ETA PKG',blank=True, null=True)
    ata_pkg = models.DateTimeField(verbose_name='ATA PKG',blank=True, null=True)
    etb_pkg = models.DateField(verbose_name='ETB PKG',blank=True, null=True)
    atb_pkg = models.DateTimeField(verbose_name='ATA PKG',blank=True, null=True)
    etd_pkg = models.DateField(verbose_name='ETD PKG',blank=True, null=True)
    atd_pkg = models.DateTimeField(verbose_name='ATD PKG',blank=True, null=True)
    berthing_delay_pkg = models.CharField(max_length=15,blank=True, null=True) 


    week_cgp_2 = models.CharField(max_length=10, verbose_name='Week CGP-2',blank=True, null=True)
    terminal_cgp_2 = models.CharField(max_length=100,blank=True, null=True)
    
    eta_cgp_2 = models.DateField(verbose_name='ETA CGP-2',blank=True, null=True)
    ata_cgp_2 = models.DateTimeField(verbose_name='ATA CGP-2',blank=True, null=True)
    etb_cgp_2 = models.DateField(verbose_name='ETB CGP-2',blank=True, null=True)
    atb_cgp_2 = models.DateTimeField(verbose_name='ATA CGP-2',blank=True, null=True)
    etd_cgp_2 = models.DateField(verbose_name='ETD CGP-2',blank=True, null=True)
    atd_cgp_2 = models.DateTimeField(verbose_name='ATD CGP-2',blank=True, null=True)
    berthing_delay_cgp_2 = models.CharField(max_length=15,blank=True, null=True)
    voyage_complete = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.service} - {self.operator} - {self.vessel} - {self.voyage_s}"
    


    def save(self,*arg,**kwargs):
        if self.pk:
            old_data = BES_Complete.objects.get(pk=self.pk) 
            if old_data.ata_cgp != self.ata_cgp:
                self.rv1 = self.rv1 + (self.ata_cgp - old_data.ata_cgp).days #(old_data.ata_cgp_2 - self.ata_cgp).days
                self.sb_v1 = self.sb_v1 + (self.ata_cgp - old_data.ata_cgp).days #(old_data.ata_pkg - self.ata_cgp).days
            if old_data.atb_cgp != self.atb_cgp:
                self.rv2 = self.rv2 + (self.atb_cgp - old_data.atb_cgp).days #(old_data.atb_cgp_2 - self.atb_cgp).days
                self.sb_v2 = self.sb_v2 + (self.atb_cgp - old_data.atb_cgp).days #(old_data.atb_pkg - self.atb_cgp).days
                self.berthing_delay_cgp = get_berthing_delay(self.eta_cgp, self.atb_cgp)
            if old_data.atd_cgp != self.atd_cgp:
                self.rv3 = self.rv3 + (self.atd_cgp - old_data.atd_cgp).days #(old_data.atd_cgp_2 - self.atd_cgp).days
                self.sb_v3 =self.sb_v3 + (self.atd_cgp - old_data.atd_cgp).days #(old_data.atd_pkg - self.atd_cgp).days
            if old_data.ata_sin != self.ata_sin:
                print("ata_sin changed")
            if old_data.atb_sin != self.atb_sin:
                
                self.berthing_delay_sin = get_berthing_delay(self.eta_sin, self.atb_sin)
            if old_data.atd_sin != self.atd_sin:
                print("atd_sin changed")
            if old_data.ata_pkg != self.ata_pkg:
                self.sb_v1 = self.sb_v1 + (self.ata_pkg - old_data.ata_pkg).days #(self.ata_pkg - old_data.ata_cgp).days
                self.nb_v1 = self.nb_v1 + (self.ata_pkg - old_data.ata_pkg).days #(old_data.ata_cgp_2 - self.ata_pkg).days
            if old_data.atb_pkg != self.atb_pkg:
                self.sb_v2 = self.sb_v2 + (self.atb_pkg - old_data.atb_pkg).days #(self.atb_pkg - old_data.atb_cgp).days
                self.nb_v2 = self.nb_v2 + (self.atb_pkg - old_data.atb_pkg).days #(old_data.atb_cgp_2 - self.atb_pkg).days
                self.berthing_delay_pkg = get_berthing_delay(self.eta_pkg, self.atb_pkg)
            if old_data.atd_pkg != self.atd_pkg:
                self.sb_v3 = self.sb_v3 + (self.atd_pkg - old_data.atd_pkg).days #(self.atd_pkg - old_data.atd_cgp).days
                self.nb_v3 = self.nb_v3 + (self.atd_pkg - old_data.atd_pkg).days#(old_data.atd_cgp_2 - self.atd_pkg).days
            if old_data.ata_cgp_2 != self.ata_cgp_2:
                self.rv1 = self.rv1 + (self.ata_cgp_2 - old_data.ata_cgp_2).days #(self.ata_cgp_2 - old_data.ata_cgp).days    
                self.nb_v1 = self.nb_v1 + (self.ata_cgp_2 - old_data.ata_cgp_2).days #(self.ata_cgp_2 - old_data.ata_pkg).days
            if old_data.atb_cgp_2 != self.atb_cgp_2:
                self.rv2 = self.rv2 + (self.atb_cgp_2 - old_data.atb_cgp_2).days #(self.atb_cgp_2 - old_data.atb_cgp).days
                self.nb_v2 = self.nb_v2 + (self.atb_cgp_2 - old_data.atb_cgp_2).days#(self.atb_cgp_2 - old_data.atb_pkg).days
                self.berthing_delay_cgp_2 = get_berthing_delay(self.eta_cgp_2, self.atb_cgp_2)
            if old_data.atd_cgp_2 != self.atd_cgp_2:
                self.rv3 = self.rv3 + (self.atd_cgp_2 - old_data.atd_cgp_2).days#(self.atd_cgp_2 - old_data.atd_cgp).days
                self.nb_v3 = self.nb_v3 + (self.atd_cgp_2 - old_data.atd_cgp_2).days #(self.atd_cgp_2 - old_data.atd_pkg).days
        
        super().save(*arg, **kwargs)





class CCE_Complete(models.Model):


    operator = models.CharField(max_length=100,blank=True, null=True)
    service = models.CharField(max_length=10,blank=True, null=True)
    rv1 = models.IntegerField(blank=True, null=True)
    sb_v1 = models.IntegerField(blank=True, null=True)
    nb_v1 = models.IntegerField(blank=True, null=True)
    rv2 = models.IntegerField(blank=True, null=True)
    sb_v2 = models.IntegerField(blank=True, null=True)
    nb_v2 = models.IntegerField(blank=True, null=True)
    rv3 = models.IntegerField(blank=True, null=True)
    sb_v3 = models.IntegerField(blank=True, null=True)
    nb_v3 = models.IntegerField(blank=True, null=True)

    week_cgp = models.CharField(max_length=10, verbose_name='Week CGP',blank=True, null=True)
    only_vessel_name = models.CharField(max_length=100,blank=True, null=True)
    vessel_code = models.CharField(max_length=20,blank=True, null=True)
    vessel = models.CharField(max_length=100,blank=True, null=True)
    voyage_s = models.CharField(max_length=10, verbose_name='Voyage-S',blank=True, null=True)
    voyage_s_with_code = models.CharField(max_length=20, verbose_name='Voyage-S with Code',blank=True, null=True)
    terminal_cgp = models.CharField(max_length=100,blank=True, null=True)

    
    
    # Date fields for ETA, ETB, and ETD
    eta_cgp = models.DateField(verbose_name='ETA CGP',blank=True, null=True)
    ata_cgp = models.DateTimeField(verbose_name='ATA CGP',blank=True, null=True)
    etb_cgp = models.DateField(verbose_name='ETB CGP',blank=True, null=True)
    atb_cgp = models.DateTimeField(verbose_name='ATB CGP',blank=True, null=True)
    etd_cgp = models.DateField(verbose_name='ETD CGP',blank=True, null=True)
    atd_cgp = models.DateTimeField(verbose_name='ATD CGP',blank=True, null=True)

    berthing_delay_cgp = models.CharField(max_length=15,blank=True, null=True)


    week_cmb = models.CharField(max_length=10, verbose_name='Week CMB',blank=True, null=True)
    voyage_n = models.CharField(max_length=10, verbose_name='Voyage-N',blank=True, null=True)
    voyage_n_with_code = models.CharField(max_length=20, verbose_name='Voyage-N with Code',blank=True, null=True)
    terminal_cmb = models.CharField(max_length=100,blank=True, null=True)
    
    eta_cmb = models.DateField(verbose_name='ETA CMB',blank=True, null=True)
    ata_cmb = models.DateTimeField(verbose_name='ATA CMB',blank=True, null=True)
    etb_cmb = models.DateField(verbose_name='ETB CMB',blank=True, null=True)
    atb_cmb = models.DateTimeField(verbose_name='ATA CMB',blank=True, null=True)
    etd_cmb = models.DateField(verbose_name='ETD CMB',blank=True, null=True)
    atd_cmb = models.DateTimeField(verbose_name='ATA CMB',blank=True, null=True)
    berthing_delay_cmb = models.CharField(max_length=15,blank=True, null=True)
    
    week_cgp_2 = models.CharField(max_length=10, verbose_name='Week CGP-2',blank=True, null=True)
    terminal_cgp_2 = models.CharField(max_length=100,blank=True, null=True)   
    eta_cgp_2 = models.DateField(verbose_name='ETA CGP-2',blank=True, null=True)
    ata_cgp_2 = models.DateTimeField(verbose_name='ATA CGP-2',blank=True, null=True)
    etb_cgp_2 = models.DateField(verbose_name='ETB CGP-2',blank=True, null=True)
    atb_cgp_2 = models.DateTimeField(verbose_name='ATA CGP-2',blank=True, null=True)
    etd_cgp_2 = models.DateField(verbose_name='ETD CGP-2',blank=True, null=True)
    atd_cgp_2 = models.DateTimeField(verbose_name='ATA CGP-2',blank=True, null=True)
    berthing_delay_cgp_2 = models.CharField(max_length=15,blank=True, null=True)  
    voyage_complete = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.operator} - {self.service} - {self.vessel} - {self.voyage_s}"
    


    def save(self,*arg,**kwargs):
        if self.pk:
            old_data = CCE_Complete.objects.get(pk=self.pk) 
            if old_data.ata_cgp != self.ata_cgp:
                self.rv1 = self.rv1 + (self.ata_cgp - old_data.ata_cgp).days #(old_data.ata_cgp_2 - self.ata_cgp).days
                self.sb_v1 = self.sb_v1 + (self.ata_cgp - old_data.ata_cgp).days #(old_data.ata_pkg - self.ata_cgp).days
            if old_data.atb_cgp != self.atb_cgp:
                self.rv2 = self.rv2 + (self.atb_cgp - old_data.atb_cgp).days #(old_data.atb_cgp_2 - self.atb_cgp).days
                self.sb_v2 = self.sb_v2 + (self.atb_cgp - old_data.atb_cgp).days #(old_data.atb_pkg - self.atb_cgp).days
                self.berthing_delay_cgp = get_berthing_delay(self.eta_cgp, self.atb_cgp)
            if old_data.atd_cgp != self.atd_cgp:
                self.rv3 = self.rv3 + (self.atd_cgp - old_data.atd_cgp).days #(old_data.atd_cgp_2 - self.atd_cgp).days
                self.sb_v3 =self.sb_v3 + (self.atd_cgp - old_data.atd_cgp).days #(old_data.atd_pkg - self.atd_cgp).days
            
            if old_data.ata_cmb != self.ata_cmb:
                self.sb_v1 = self.sb_v1 + (self.ata_cmb - old_data.ata_cmb).days #(self.ata_pkg - old_data.ata_cgp).days
                self.nb_v1 = self.nb_v1 + (self.ata_cmb - old_data.ata_cmb).days #(old_data.ata_cgp_2 - self.ata_pkg).days
            if old_data.atb_cmb != self.atb_cmb:
                self.sb_v2 = self.sb_v2 + (self.atb_cmb - old_data.atb_cmb).days #(self.atb_pkg - old_data.atb_cgp).days
                self.nb_v2 = self.nb_v2 + (self.atb_cmb - old_data.atb_cmb).days #(old_data.atb_cgp_2 - self.atb_pkg).days
                self.berthing_delay_cmb = get_berthing_delay(self.eta_pkg, self.atb_pkg)
            if old_data.atd_cmb != self.atd_cmb:
                self.sb_v3 = self.sb_v3 + (self.atd_cmb - old_data.atd_cmb).days #(self.atd_pkg - old_data.atd_cgp).days
                self.nb_v3 = self.nb_v3 + (self.atd_cmb - old_data.atd_cmb).days#(old_data.atd_cgp_2 - self.atd_pkg).days
            if old_data.ata_cgp_2 != self.ata_cgp_2:
                self.rv1 = self.rv1 + (self.ata_cgp_2 - old_data.ata_cgp_2).days #(self.ata_cgp_2 - old_data.ata_cgp).days    
                self.nb_v1 = self.nb_v1 + (self.ata_cgp_2 - old_data.ata_cgp_2).days #(self.ata_cgp_2 - old_data.ata_pkg).days
            if old_data.atb_cgp_2 != self.atb_cgp_2:
                self.rv2 = self.rv2 + (self.atb_cgp_2 - old_data.atb_cgp_2).days #(self.atb_cgp_2 - old_data.atb_cgp).days
                self.nb_v2 = self.nb_v2 + (self.atb_cgp_2 - old_data.atb_cgp_2).days#(self.atb_cgp_2 - old_data.atb_pkg).days
                self.berthing_delay_cgp_2 = get_berthing_delay(self.eta_cgp_2, self.atb_cgp_2)
            if old_data.atd_cgp_2 != self.atd_cgp_2:
                self.rv3 = self.rv3 + (self.atd_cgp_2 - old_data.atd_cgp_2).days#(self.atd_cgp_2 - old_data.atd_cgp).days
                self.nb_v3 = self.nb_v3 + (self.atd_cgp_2 - old_data.atd_cgp_2).days #(self.atd_cgp_2 - old_data.atd_pkg).days
        
        super().save(*arg, **kwargs)





    







