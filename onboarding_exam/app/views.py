from django.shortcuts import render,redirect
from config.settings import sf_client
from app.forms import LeadForm
from pprint import pprint
from  simple_salesforce import format_soql;
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
               'Email' : form.cleaned_data['Email'],
               'LeadSource' : 'Web'
           }) 
 
           return redirect("app:lead_detail",lead_id=created_lead['id'])
        # Need Error handling Code
        
        else : 
            return render(request,"leadcreate.html",{'form':form})
        
def lead_detail(request,lead_id) :

    # GET ALL FIELDS    
    #lead_fields = [field['name'] for field in sf_client.Lead.describe()['fields']]
    #str_fields = (', ').join(lead_fields)
    #searchedLead = sf_client.query(format_soql('SELECT {str_fields} FROM Lead WHERE Id={last_id}',str_fields=str_fields,last_id=lead_id))

    searchedLead = sf_client.query(
        format_soql('SELECT Id,Name,Company,Phone,Email,Status,LeadSource FROM Lead WHERE id={lead_id}',lead_id=lead_id)
        )
    context = {
        'lead' : searchedLead['records'][0]
    }

    
    return render(request,'lead_detail.html',context)

def account_list(request):
    searchedAccounts = sf_client.query_all(format_soql('SELECT Id,Name FROM Account'))['records']

    context = {
        'account_list' : searchedAccounts
    }

    return render(request,'account_list.html',context) 

#TODO : Related Opp Query 
def account_detail(request,account_id) :   
    account_info = sf_client.query(format_soql('SELECT Name, Industry, Type, Phone, Website, BillingCity, BillingCountry, BillingState, BillingPostalCode, BillingStreet \
                                               FROM Account WHERE Id={account_id}',account_id= account_id))['records'][0]
                                   
    opps = sf_client.query(format_soql('SELECT Id, (SELECT Id, Name , Amount FROM Opportunities WHERE StageName=\'Closed Won\' ORDER BY Amount DESC LIMIT 1) FROM Account WHERE Id={account_id}',account_id=account_id))['records'][0]['Opportunities']
    context = {
        'account' : account_info,
        'opps' : opps
    }

    return render(request,'account_detail.html',context)