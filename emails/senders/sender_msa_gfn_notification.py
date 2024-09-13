from pandaspro import create_mail_class
from fadfpdata.emails.engines.msa_gfn_notification import msa_gfn_notification

msa_gfn_Sender = create_mail_class(
    r'C:\Users\xli7\Desktop\python_projects\fadfpdata\emails\templates\msa_gfn_notification.html',
    msa_gfn_notification
)
myemail = msa_gfn_Sender(ifscode=199)
show = myemail.display()
del create_mail_class
del msa_gfn_notification