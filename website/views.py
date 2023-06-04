from flask import Blueprint, render_template, redirect, url_for,request,flash
from .models import Movie,Venue,User,Admin,Booking
from . import db
from flask_login import login_required,current_user,login_manager
from sqlalchemy import func
import matplotlib
import numpy as np
matplotlib.use('Agg')    #used to covert it as non-GUI fast rendering
import matplotlib.pyplot as plt
import operator

views = Blueprint('views', __name__)


@views.route('/login_failed')
@login_required
def login_failed():
    return redirect(url_for('auth.login_get_user'))


@views.route('/signup_failed')
@login_required
def signup_failed():
    return redirect(url_for('auth.signup_get_admin'))

@views.route('/city_user')
@login_required
def city_user():
    return render_template("usercity.html",user=current_user)

@views.route('/city_admin')
@login_required
def city_admin():
    return render_template("admincity.html",admin=current_user)

@views.route('/city_user1',methods=['GET','POST'])
@login_required
def city_user1():
    if request.method == 'POST':
        user1 = User.query.filter_by(user_name = current_user.user_name).first()
        user1.user_city = request.form.get("city")
        db.session.commit()
    return redirect(url_for('views.user11'))

@views.route('/city_admin1',methods=['GET','POST'])
@login_required
def city_admin1():
    if request.method == 'POST':
        admin1 = Admin.query.filter_by(admin_name = current_user.admin_name).first()
        admin1.admin_city = request.form.get("city")
        db.session.commit()
    return redirect(url_for('views.add_movies')) 


@views.route('/sign_up_success')
@login_required
def sign_up_success():
    return redirect(url_for('auth.login_get_user'))

@views.route('/sign_up_failed')
@login_required
def sign_up_failed():
    return redirect(url_for('auth.signup_admin'))
 

@views.route('/add_movies',methods=['GET','POST'])
@login_required
def add_movies():
    try:
        if request.method == 'POST':
            movie_n = request.form.get("moviename")
            movie_m_c = request.form.get("moviecapacity")
            movie_t_c = request.form.get("ticketcost")
            movie_s = request.form.get("showtime")
            movie_l = request.form.get("length")
            movie_v = request.form.get("venue")
            venue = Venue.query.all()
            movie = Movie.query.all()
            for i in movie:
                if(str(i.movie_name) == str(movie_n) and int(i.movie_capacity) == int(movie_m_c) and str(i.movie_show_time) == str(movie_s) and str(i.movie_venue) == str(movie_v)):
                    flash("Movie already Exists !!!")
                    return render_template("Addmovies.html",admin=current_user)
                
            for row in venue:
                if(row.venue_name == movie_v):
                    new_movie = Movie(movie_name = movie_n, movie_capacity = movie_m_c, movie_ticket_cost = movie_t_c , movie_show_time = movie_s, movie_length = movie_l, movie_venue = movie_v )
                    db.session.add(new_movie)
                    db.session.commit()
                    flash("Movie added Successfully !!!")
                    return redirect(url_for('views.add_movies')) 
                
            flash("Entered venue doesn't exists, create it first !!!")
            return redirect(url_for('views.add_venue'))   
        return render_template("Addmovies.html",admin=current_user)
    except:
        return "<h2>Something went wrong.</h2>"


@views.route('/add_venue',methods=['GET','POST'])
@login_required
def add_venue():
    try:
        if request.method == 'POST':
            Venue_n = request.form.get("Venuename")
            Venue_c = request.form.get("Capacity")
            Venue_l = request.form.get("venuelocation")
            Venue_p = request.form.get("venueplace")
            Venue_r = request.form.get("Rating")
            new_venue = Venue( venue_name = Venue_n, venue_capacity = Venue_c,venue_rating = Venue_r,venue_location = Venue_l,venue_city = Venue_p )
            db.session.add(new_venue)
            db.session.commit()
            flash("Venue added Successfully !!!")
            return redirect(url_for('views.add_venue'))
    except:
        flash("Venue already exists !!!")
        return redirect(url_for('views.add_venue'))
    return render_template("AddVenue.html",admin=current_user)


@views.route('/view_movies',methods=['GET','POST'])
@login_required
def view_movies():
    movie=Movie.query.all()
    return render_template("viewmovies.html", movie=movie,admin=current_user)

@views.route('/view_venue',methods=['GET','POST'])
@login_required
def view_venue():
    venue=Venue.query.all()
    return render_template("viewvenue.html",venue=venue,admin=current_user)

@views.route('/remove_movie/<int:id>')
@login_required
def remove_movie(id):
    movie_remove = Movie.query.get(id)
    db.session.delete(movie_remove)
    db.session.commit()
    return redirect(url_for("views.view_movies"))

@views.route('/remove_venue/<int:id>')
@login_required
def remove_venue(id):
    venue_remove = Venue.query.get(id)
    id1=id
    venuename = venue_remove.venue_name
    print(venuename)
    movie = Movie.query.all()
    list_m = []

    for rows in movie:
        if(rows.movie_venue == venuename):
            list_m.append(rows)

    if list_m != []:
        for i in list_m:
            db.session.delete(i)
            db.session.commit()
        return redirect(url_for("views.delete_venue_row",id=id1))
    
    if list_m == []:
        venue_remove = Venue.query.get(id)
        db.session.delete(venue_remove)
        db.session.commit()
        return redirect(url_for("views.view_venue")) 


@views.route('/delete_venue_row/<int:id>')
@login_required
def delete_venue_row(id):
    venue_remove = Venue.query.get(id)
    db.session.delete(venue_remove)
    db.session.commit()
    return redirect(url_for("views.view_venue"))


@views.route('/update_movie/<int:id>',methods=['GET','POST'])
@login_required
def update_movie(id):
    movie_update = Movie.query.get(id)
    movie = Movie.query.all()
    if request.method == 'POST':  
        venue = Venue.query.all()
        movie_v = request.form.get("venue") 
        movie_n = request.form.get("moviename")
        movie_m_c = request.form.get("moviecapacity")
        movie_s = request.form.get("showtime")
        movie_t_c = request.form.get("ticketcost")
        movie_l = request.form.get("length")
    for i in movie:
        if(str(i.movie_name) == str(movie_n) and int(i.movie_capacity) == int(movie_m_c) and str(i.movie_show_time) == str(movie_s) and str(i.movie_venue) == str(movie_v) and str(i.movie_length) == str(movie_l) and int(i.movie_ticket_cost) == int(movie_t_c)):
            flash("Movie already Exists !!!")
            return redirect(url_for("views.view_movies"))
        
    # update form venue should exists in venue table
    for row in venue:
        if(row.venue_name == movie_v):
            movie_update.movie_name = request.form.get("moviename")
            movie_update.movie_capacity = request.form.get("moviecapacity")
            movie_update.movie_ticket_cost = request.form.get("ticketcost")
            movie_update.movie_show_time = request.form.get("showtime")
            movie_update.movie_length = request.form.get("length")
            movie_update.movie_venue = request.form.get("venue")
            db.session.commit()
            flash("Details updated successfully !!!")
            return redirect(url_for("views.view_movies")) 
            
    flash("Entered venue doesn't exists, create it first !!!")
    return redirect(url_for('views.add_venue'))

@views.route('/update_venue/<int:id>',methods=['GET','POST'])
@login_required
def update_venue(id):
    venue_update = Venue.query.get(id)
    if request.method == 'POST':
        venue_update.venue_name = request.form.get("venuename")
        venue_update.venue_capacity = request.form.get("venuecapacity")
        venue_update.venue_location = request.form.get("venuelocation")
        venue_update.venue_city = request.form.get("venueplace")
        venue_update.venue_rating = request.form.get("venuerating")
        db.session.commit()
        flash("Details updated successfully !!!")
        return redirect(url_for("views.view_venue")) 


@views.route('/user11', methods=['GET', 'POST'])
@login_required
def user11():
    movie = Movie.query.group_by(Movie.movie_name)
    u_city = current_user.user_city
    venue = Venue.query.all()
    v_list = []
    for i in venue:
        if i.venue_city.lower() == u_city.lower():
            v_list.append(i.venue_name)
    m_list = []        
    for i in movie:
        for j in v_list:
            if i.movie_venue == j:
                m_list.append(i)                   
    return render_template("user1.html", m1 = m_list,user=current_user) 

@views.route('/all_movies', methods=['GET', 'POST'])
@login_required
def all_movies():
    movie = Movie.query.group_by(Movie.movie_name)
    m_list = []
    for i in movie:
        m_list.append(i)
    return render_template("allmovies.html", m1 = m_list,user=current_user)

@views.route('/user22/<string:name>', methods=['GET', 'POST'])
@login_required
def user22(name):
    try:
        m1 = name
        movie = Movie.query.filter(Movie.movie_name == name).all()
        d={}
        for rows in movie:
            venue=rows.movie_venue
            venue1 = Venue.query.filter(Venue.venue_name == venue).all()
            for i in venue1:
                venuerating =i.venue_rating
                venuelocation =i.venue_location
                venueplace =i.venue_city
                d[rows.movie_id] = [rows.movie_venue,rows.movie_capacity,venuerating,venuelocation,venueplace]
        return render_template("user2.html",movie_name =m1, m3 = d ,user=current_user)
    except:
        return "<h2>Something went wrong.</h2>"

@views.route('/booking33/<int:id>', methods=['GET', 'POST'])
@login_required
def booking33(id):
    try:
        u5 = Movie.query.get(id)
        u8 = u5.movie_capacity
        u7 = u5.movie_name
        u6 = u5.movie_ticket_cost
        u4 = u5.movie_show_time
        u3 = u5.movie_venue 
        u2 = id  
        return render_template("userbooking.html", movie_capacity = u8 , movie_name = u7 , movie_ticket_cost = u6 , movie_show_time = u4 , movie_venue = u3 , movie_id = u2,user=current_user)
    except:
        return "<h2>Something went wrong.</h2>"

@views.route('/bookingconfirm44/<int:id>', methods=['GET', 'POST'])
@login_required
def bookingconfirm44(id):
    y1 = Movie.query.get(id)
    y2 = y1.movie_ticket_cost
    y3 = y1.movie_venue
    y4 = y1.movie_name
    y5 = y1.movie_show_time
    y6 = y1.movie_capacity
    y9 = id
    if request.method == 'POST':
        t_s = request.form.get("totalseats")
        y7 = int(int(y2)*int(t_s))
        y8 = int(int(y6)-int(t_s))
        if(y8>=0):
            y1.movie_capacity = y8
        else:
            return "<h1>erroe</h1>" 
    return render_template("userbookingconfirm.html",new_capacity = y8 , movie_name = y4 , movie_ticket_cost = y2 , movie_show_time = y5 , movie_venue = y3 , movie_id = y9, total_cost =y7 , total_seats = t_s ,user=current_user)    


@views.route('/confirm55/<int:id>/<int:id1>', methods=['GET', 'POST'])
@login_required
def confirm55(id,id1):
    t_s =id1
    q1 = Movie.query.get(id)
    q2 = q1.movie_ticket_cost
    q3 = q1.movie_venue
    q4 = q1.movie_name
    q5 = q1.movie_show_time
    q6 = q1.movie_capacity
    q12 = q1.movie_length
    q9 = id
    x = int(t_s)
    q10=[]
    for i in range(x):
        q10.append(i)
    q7 = int(int(q2)*int(t_s))
    q8 = int(int(q6)-int(t_s))
    if(q8>=0):
        q1.movie_capacity = q8
        db.session.commit()
        new_booking = Booking( booking_user = current_user.user_name , booking_movie_name = q4 , booking_venue = q3, booking_time = q5 , booking_seats = t_s, booking_cost = q7 )
        db.session.add(new_booking)
        db.session.commit()
    else:
        return "<h1>error</h1>"    
    return render_template("userconfirm.html",new_capacity = q8 , movie_name = q4 , movie_ticket_cost = q2 , movie_show_time = q5 , movie_venue = q3 , movie_id = q9, total_cost =q7 , total_seats = t_s , q11 = q10,movie_length =q12,user=current_user)

@views.route('/view_booking',methods=['GET', 'POST'])
@login_required
def view_booking():
    try:
        book = Booking.query.filter(Booking.booking_user == current_user.user_name).all()
        return render_template("userviewbooking.html", m5 = book , user=current_user)
    except:
        return "<h2>Something went wrong.</h2>"

@views.route('/button_rating/<int:id>/<int:id1>',methods=['GET', 'POST'])
@login_required
def button_rating(id,id1):
    button_id = int(id)
    result = Booking.query.get(id1)
    result.booking_rateing = button_id
    db.session.commit()
    return redirect(url_for('views.view_booking'))   

@views.route('/delete_booking/<int:id>',methods=['GET', 'POST'])
@login_required
def delete_booking(id):
    delete = Booking.query.get(id)
    seats = delete.booking_seats
    movie = Movie.query.all()
    for rows in movie:
        if(rows.movie_name == delete.booking_movie_name and rows.movie_venue == delete.booking_venue):
            rows.movie_capacity += int(seats)
            db.session.commit()
    db.session.delete(delete)
    db.session.commit()
    return redirect(url_for("views.view_booking")) 


@views.route('/search_movie',methods=['GET', 'POST'])
@login_required
def search_movie():
        if request.method == 'POST':
            movie = request.form.get("searchmovie")
            
            movie1 = Movie.query.filter(func.lower(Movie.movie_name) == func.lower(movie)).all()
            #movie1 list
            #case-1 movie name
            movielist=[]
            for i in movie1:
                movielist.append(i)
            movies={}
            for x in movie1:
                movies[x.movie_id]=[]
                venue = x.movie_venue
                venuetable=Venue.query.all()
                for i in venuetable:
                    if(i.venue_name == venue):
                        movies[x.movie_id]=[i.venue_city]
            #case-2 movie-tag 
            if(movie1 == []):
                movie2 = Movie.query.filter(func.lower(Movie.movie_tag) == func.lower(movie)).all()
                taglist=[]
                for i in movie2:
                    taglist.append(i)  
                moviestag={}
                for x in movie2:
                    moviestag[x.movie_id]=[]
                    venue = x.movie_venue
                    venuetable=Venue.query.all()
                    for i in venuetable:
                        if(i.venue_name == venue):
                            moviestag[x.movie_id]=[i.venue_city]
                #case-3 city
                if (movie2 == []):
                    venuecity={}
                    movie3 = Venue.query.filter(func.lower(Venue.venue_city) == func.lower(movie)).all()
                    for i in movie3:
                        venuecity[i.venue_name]=[]
                    moviecity=Movie.query.all()
                    citylist=[]
                    for x in moviecity:
                        for key in venuecity:
                            if(x.movie_venue == key):
                                venuecity[key]=[x]       
                                citylist.append(x)         
                    return render_template("search.html",user=current_user , m3 = citylist, movie = movie)
                return render_template("search.html",user=current_user , m1 = taglist, m2=moviestag,movie = movie)      
            return render_template("search.html",user=current_user , m1 = movielist, m2=movies,movie = movie)
          
                                                                                       
@views.route('/trends')
@login_required
def trends():
    try:
        movie = Movie.query.group_by(Movie.movie_name)   #query
        movie_list=[]
        for i in movie:
            movie_list.append(i.movie_name)
        d={}
        for i in movie_list:
            d[i]=0
        booking=Booking.query.all()

        for i in movie_list:
            count = 0
            sum = 0
            for j in booking:
                if(i==j.booking_movie_name):
                    sum = sum + int(j.booking_rateing)
                    count = count + 1        
                    avg = sum/count
                    d[i] = int(avg)            

        # for movie rating

        for key,value in d.items():
            moviename = Movie.query.filter(Movie.movie_name == key).all()
            for i in moviename:
                i.movie_rating = value
                db.session.commit()

        # for highest rated movie

        max=0
        max_list=[]
        for key,value in d.items():
            if( max<=value):
                max=value
        
        for key,value in d.items():
            if(max==value):
                max_list.append(key)

        # for sorted rating dict

        sorted_d={}
        sorted_d = dict( sorted(d.items(), key=operator.itemgetter(1),reverse=True))


        x=[]
        y=[]
        x = list(d.keys())
        y = list(d.values())     
    

        fig = plt.figure(figsize = (10, 5))

        # creating the bar plot
        plt.bar(x, y, color=['#452c63', '#4B0082' , '#662d91'] , width = 0.4) 
        plt.xticks(fontsize=15)
        plt.xticks(fontsize=15)   
        plt.xlabel("Movies",fontsize=17,labelpad=20)
        plt.ylabel("Ratings",fontsize=17,labelpad=20)
        plt.title("Ratings of Movies",fontsize=22,fontweight='bold',pad=20)
        plt.tight_layout()
        plt.savefig('website/static/graph1.jpeg')

        # movies and no of seats

        a={}
        for i in movie_list:
            a[i]=0

        for i in movie_list:
            total = 0
            for j in booking:
                if(i==j.booking_movie_name):
                    total = total + int(j.booking_seats)        
                    a[i] = total

        # for max seats

        max1=0
        max_list1=[]
        for key,value in a.items():
            if( max1<=value):
                max1=value
        
        for key,value in a.items():
            if(max1==value):
                max_list1.append(key)


        # for sorted seats dict

        sorted_s={}
        sorted_s = dict( sorted(a.items(), key=operator.itemgetter(1),reverse=True))

        #for top booked movies 

        firstkey = list(sorted_s.keys())[0]
        secondkey = list(sorted_s.keys())[1]
        thirdkey = list(sorted_s.keys())[2]
        topbooked=[firstkey,secondkey,thirdkey]

        z = list(a.values())

        fig1, ax = plt.subplots(figsize=(6, 6))
        ax.pie(z, labels=x, autopct='%.1f%%',colors = ( "orange", "cyan", "brown", "grey", "indigo", "beige"),
        wedgeprops={'linewidth': 8.0, 'edgecolor': 'white'},
        textprops={'size': 'medium'})
        ax.set_title('Most seen movies', fontsize=18,fontweight='bold')
        plt.tight_layout()
        plt.savefig('website/static/graph2.jpeg')
        # plt.show() 
        
        b=['Super Hit','Hit','Average']
        category={}
        for x in b:
            category[x]=[]
    

        for key,value in d.items():
            if(int(value)>=4):
                category['Super Hit'].append(key)
            elif(3<=int(value)<4):
                category['Hit'].append(key)
            else:
                category['Average'].append(key) 

        movie_tag={}

        for key,value in category.items():
            for i in value:
                movie_tag[i]=key


        for key,value in movie_tag.items():    
            movietag = Movie.query.filter(Movie.movie_name == key).all()
            for i in movietag:
                i.movie_tag = value
                db.session.commit()
                

        c = list(category.values())           

        return render_template("trends.html" , user=current_user , category1 = category , ratingdict = sorted_d ,highrating = max_list,seatsdict = sorted_s,highseats = max_list1,topbooked = topbooked)
    except:
        return "<h2>Something went wrong.</h2>"

        
    


    

