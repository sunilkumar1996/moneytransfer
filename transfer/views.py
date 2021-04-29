
from django.shortcuts import render 
  
def home(request): 
    
    return render(request, "home/transfer.html") 
def howtowork(request): 
    
    return render(request, "home/howtowork.html") 



def mobiletransfer(request): 
    
    return render(request, "home/mobiletransfer.html")     


def about(request): 
    
    return render(request, "home/about.html")         
