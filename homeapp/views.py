from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage # as fs
from django.contrib import messages
from django.contrib.auth.models import User
from homeapp.models import *
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

# Create your views here.
# Patient funtion is used to sign up a patient
def patient(request):
    if request.method == "POST" and request.FILES['pic']:
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')        
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirmpassword = request.POST.get('confirmpassword')
        address = request.POST.get('address')
        city = request.POST.get('city')
        state = request.POST.get('state')
        zip = request.POST.get('zip')

        try:
            if not username.isalnum():
                messages.warning(request, "User name should only contain letters and numbers")
                return redirect('/patient')

            if User.objects.filter(username=username).first():
                messages.warning(request, 'Username is taken!')
                return redirect('/patient')
            
            if User.objects.filter(email=email).first():
                messages.warning(request, 'Email is taken!')
                return redirect('/patient')    
            
            if password != confirmpassword:
                messages.warning(request, 'The Confirm Password not matched with the Password!!')
                return redirect('/patient')

            user_obj = User(username=username, first_name=firstname, last_name=lastname, email=email)
            user_obj.set_password(password)
            user_obj.save()

            pic = request.FILES['pic']
            fs = FileSystemStorage()
            filename = fs.save(pic.name, pic) # Storing image in database with auto generated name:
            url = fs.url(filename)

            current_user = User.objects.filter(username=username).first()            
            patient_obj = Patient(user=current_user, pic=url, address=address, city=city, state=state, zip=zip)
            patient_obj.save()
            messages.warning(request, f'{firstname}, you have successfully sign up.')
            return redirect('/')

        except Exception as e:
            messages.warning(request, 'Sorry for incenvinence!')
            messages.info(request, f'An exception occured : {e}')
            return redirect('/patient')

        # print(firstname, lastname, pic, username,email,password,confirmpassword,address,city,state,zip)
    return render(request, 'homeapp/patient.html')

# Doctor funtion is used to sign up a doctor
def doctor(request):
    if request.method == "POST":
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        pic = request.POST.get('pic')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirmpassword = request.POST.get('confirmpassword')
        address = request.POST.get('address')
        city = request.POST.get('city')
        state = request.POST.get('state')
        zip = request.POST.get('zip')

        try:
            if not username.isalnum():
                messages.warning(request, "User name should only contain letters and numbers")
                return redirect('/doctor')

            if User.objects.filter(username=username).first():
                messages.warning(request, 'Username is taken!')
                return redirect('/doctor')
            
            if User.objects.filter(email=email).first():
                messages.warning(request, 'Email is taken!')
                return redirect('/doctor')    
            
            if password != confirmpassword:
                messages.warning(request, 'The Confirm Password not matched with the Password!!')
                return redirect('/doctor')

            user_obj = User(username=username, first_name=firstname, last_name=lastname, email=email, is_staff=True)
            user_obj.set_password(password)
            user_obj.save()

            pic = request.FILES['pic']
            fs = FileSystemStorage()
            filename = fs.save(pic.name, pic) # Storing image in database with auto generated name:
            url = fs.url(filename)

            current_user = User.objects.filter(username=username).first()
            doctor_obj = Doctor(user=current_user, pic=url, address=address, city=city, state=state, zip=zip)
            doctor_obj.save()
            messages.warning(request, f'{firstname}, you have successfully sign up.')
            return redirect('/')

        except Exception as e:
            messages.warning(request, 'Sorry for incenvinence!')
            messages.info(request, f'An exception occured : {e}')
            return redirect('/doctor')

        # print(firstname, lastname, pic, username,email,password,confirmpassword,address,city,state,zip)
    return render(request, 'homeapp/doctor.html')

def login_user(request):
    if request.method == "POST":
        is_patient = request.POST.get('patient')
        is_doctor = request.POST.get('doctor')
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            if is_patient == 'patient':
            # print(is_patient, username, password)            
                user_obj = User.objects.filter(username=username).first()
                if user_obj is None:
                    messages.warning(request, 'User not found!')
                    return redirect('/')
                
                user = Patient.objects.filter(user=user_obj).first() 
                if user is None:
                    messages.warning(request, 'User not found!')
                    return redirect('/')          
                
                user = authenticate(username=username, password=password)
                if user is None:
                    messages.warning(request, 'Wrong password!')
                    return redirect('/')

                login(request, user)
                request.session['username'] = user.username
                request.session['type'] = is_patient
                messages.success(request, 'Your are succussfully logged in.')
                return redirect('/allposts')
        
            if is_doctor == 'doctor':
                # print(is_doctor, username, password)
                user_obj = User.objects.filter(username=username).first()
                if user_obj is None:
                    messages.warning(request, 'User not found!')
                    return redirect('/')

                user = Doctor.objects.filter(user=user_obj).first()
                if user is None:
                    messages.warning(request, 'User not found!')
                    return redirect('/')  
                
                user = authenticate(username=username, password=password)
                if user is None:
                    messages.warning(request, 'Wrong password!')
                    return redirect('/')

                login(request, user)
                request.session['username'] = user.username
                request.session['type'] = is_doctor
                messages.success(request, 'Your are succussfully logged in.')
                return redirect('/allposts')

        except Exception as e:
            messages.warning(request, 'Sorry for incenvinence!')
            messages.info(request, f'An exception occured : {e}')
            return redirect('/')

        #  = request.POST.get('')        
    return render(request, 'homeapp/login.html')

def logout_user(request):
    logout(request)
    messages.success(request, "Successfully logged out.")
    return redirect('/')    

# @login_required(login_url="/login/")
@login_required
def dashboard(request): # Useless
    try: 
        username = request.session['username']
        type = request.session['type']

        if type == 'patient':
            user = User.objects.filter(username=username).first()
            patient = Patient.objects.filter(user=user).first()

            print('patient: ',user.email, patient.city)
            context = {'user': user, 'type': patient}
            return render(request, 'homeapp/dashboard.html', context)
        
        if type == 'doctor':
            user = User.objects.filter(username=username).first()
            doctor = Doctor.objects.filter(user=user).first()

            print('doctor: ',user.email, doctor.city)
            context = {'user': user, 'type': doctor}
            return render(request, 'homeapp/dashboard.html', context)

    except Exception as e:
        messages.warning(request, 'Sorry for incenvinence!')
        messages.info(request, f'An exception occured : {e}')
        return redirect('/login')
    
    return render(request, 'homeapp/dashboard.html')

@login_required
def allposts(request):
    # allposts = Post.objects.all()
    MentalHealth = Post.objects.filter(category='mentalHealth') 
    HeartDisease = Post.objects.filter(category='heartDisease') 
    Covid19 = Post.objects.filter(category='covid19') 
    Immunization = Post.objects.filter(category='immunization') 

    mh_list = []
    for mh in MentalHealth:
        if mh.draft == False:
            mh_list.append(mh)   

    hd_list = []
    for hd in HeartDisease:
        if hd.draft == False:
            hd_list.append(hd) 

    c19_list = []
    for c19 in Covid19:
        if c19.draft == False:
            c19_list.append(c19)   
    im_list = []
    for im in Immunization:
        if im.draft == False:
            im_list.append(im)   

    context = {'mentalHealth':mh_list, 'heartDisease':hd_list, 'covid19':c19_list, 'immunization':im_list}
    return render(request, 'blog/allposts.html', context)

@login_required
def showpost(request, id):
    post = Post.objects.filter(id=id).first()

    return render(request, 'blog/showpost.html', {'post': post})

@login_required
def myposts(request):
    user = User.objects.filter(username=request.user).first()
    author = Doctor.objects.filter(user=user).first()
    myposts = Post.objects.filter(author=author) 

    return render(request, 'blog/myposts.html', {'myposts':myposts})

@login_required
def newpost(request):
    if request.method == "POST":
        author = request.POST.get("author")
        title = request.POST.get("title")
        category = request.POST.get("category")
        summary = request.POST.get("summary")
        content = request.POST.get("content")
        is_draft = request.POST.get("is_draft")

        user = User.objects.filter(username=author).first()
        writer = Doctor.objects.filter(user=user).first()

        image = request.FILES['image']
        fs = FileSystemStorage()
        filename = fs.save(image.name, image) # Storing image in database with auto generated name:
        url = fs.url(filename)

        if is_draft == 'on':
            draft = True
        else:
            draft = False

        post = Post(author=writer, title=title, image=url, category=category, summary=summary, content=content, draft=draft)
        post.save()
        messages.success(request, 'The post have been uploaded successfully.')
        return redirect('/myposts')
    return render(request, 'blog/newpost.html')

@login_required
def updatepost(request, id):
    post = Post.objects.filter(id=id).first()

    if request.method == "POST":
        postId = request.POST.get("postId")
        title = request.POST.get("title")
        category = request.POST.get("category")
        summary = request.POST.get("summary")
        content = request.POST.get("content")
        is_draft = request.POST.get("is_draft")

        post = Post.objects.filter(id=postId).first()
    
        try:
            image = request.FILES['image']
            fs = FileSystemStorage()
            filename = fs.save(image.name, image) # Storing image in database with auto generated name:
            url = fs.url(filename)
        except Exception as e:
            url = post.image

        if summary == "":
            summary = post.summary

        if content == "":
            content = post.content

        if is_draft == 'on':
            draft = True
        else:
            draft = False

        post.title = title
        post.image = url
        post.category = category
        post.summary = summary
        post.content = content
        post.draft = draft
        post.save()
        messages.success(request, 'The post have been updated successfully.')
        return redirect('/myposts')

    return render(request, 'blog/updatepost.html', {'post':post})
