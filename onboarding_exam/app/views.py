from django.shortcuts import render,redirect
from config.settings import sf_client
from app.forms import LeadForm
from pprint import pprint
def index(request):
    return redirect("app:leadcreate")

def leadcreate(request) :
    # Request method is GET
    if request.method == "GET" : 
        form = LeadForm()
        context = {
            'form': form
        }
        return render(request,"leadcreate.html",context)
    # Request method is POST
    else :
        form = LeadForm(request.POST)
        if form.is_valid() : 
           # OrderedDict([('id', '00QdM000001ffg9UAA'), ('success', True), ('errors', [])])
           created_lead = sf_client.Lead.create({
               'LastName' :form.cleaned_data['LastName'],
               'FirstName' : form.cleaned_data['FirstName'],
               'Company' : form.cleaned_data['Company'],
              'Phone' : form.cleaned_data['Phone'],
               'Email' : form.cleaned_data['Email']
           }) 
 
           return redirect("app:lead_detail",lead_id=created_lead['id'])
        # Need Error handling Code
        else : 
            return render(request,"leadcreate.html",{'form':form})
        
def lead_detail(request,lead_id) :
    searchedLead = sf_client.Lead.get(lead_id) 
    print(searchedLead)
    context = {
        'lead' : searchedLead
    }
    return render(request,'lead_detail.html',context)
