def handle_uploaded_file(f,id):  
    with open('static/upload/'+str(id)+".pdf", 'wb+') as destination:  
        for chunk in f.chunks():  
            destination.write(chunk)  