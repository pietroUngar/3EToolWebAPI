from django.db import models
import os.path


class ExcelFile(models.Model):

    id = models.AutoField(primary_key=True)
    file = models.FileField(upload_to="excel_files/")

    def __str__(self):

        return str(os.path.basename(self.file.path))

    def delete(self, *args, **kwargs):

        try:
            self.file.delete()
        except:
            pass

        super().delete(*args, **kwargs)