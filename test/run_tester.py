from tapp import app, db, posts 

from tapp.models import User, Post

if __name__ == "__main__": 

    # # create db if not exists  and add content 
    # db.create_all()
    # user1 = User(uname='bee', email='bee@go.co.jk', upass='123')
    # db.session.add( user1 ) 
    # db.session.commit()
    # user1 = User(uname='zai', email='zai@go.co.jk', upass='456')
    # db.session.add( user1 ) 
    # db.session.commit()
    # print('---- USERS ADDED ---- ') 
    # print( User.query.all() )

    # user1 = User.query.first()
    # for post in posts:
    #     p = Post(title=post['title'],
    #              #dated = post['date'],
    #              content = post['content'], 
    #              author_id = user1.id 
    #             )
    #     db.session.add( p )
    # db.session.commit()
    # print(f'---- POSTS ADDED for {user1.id}: {user1.uname}---- ') 
    # print( Post.query.all() )

    print('\n---- SUMMARY @ DB ENTRIES :: User----\n') 
    for u in User.query.all():
        print( f"{repr(u)} ")
        print("\t--- posts")
        for p in u.posts:
            print( f"\t{repr(p)}") 

    print('\n---- SUMMARY @ DB ENTRIES :: Post----\n') 
    for i, p in enumerate(Post.query.all() ):
        print( f"{repr(p)} by::{repr( p.author) } ")


    app.run(debug=True)
