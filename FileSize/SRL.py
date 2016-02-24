File Size prediction

The goal of a CDN is to serve content to end-users with high availability and high performance.
CDNs serve a large fraction of the Internet content today, including web objects (text, graphics and scripts),
Downloadable objects (media files, software, documents), applications (e-commerce, portals), live streaming media,
n-demand streaming media, and social networks.(Wikipedia)

One important process in CDNs(or generally any load balancing system) it is really important to know how much is
the response size. If you know the response size you can distribute your requests between your servers and return the response faster.
Let’s make it more clearly with an example.

Example:
Imagine we have a CDN which only serves 6 files(for simplicity)
List of files plus their size:

 
	|FileName.Extention	 |	FileSize(MB)
	|------------------		------------
	|F1.mp3				 |	 2 
	|F2.exe              |   50 
	|F3.exe              |   4
	|F4.jpg              |   10 
	|F5.MP4              |   3 
	|F6.png              |   1 

   
 Also we have 2 servers inside this CDN(A and B). Now lets say we are getting all these request in one time(simultaneously)

	

	      Request
			||
			||
			||
			/\
		   /  \
		  /    \
		 /      \
    _______     _______         
   |   A   |   |   B   |   
    ¯¯¯¯¯¯¯     ¯¯¯¯¯¯¯   




What is the Problem? How can I distribute my request between my servers with the minimum wait time?

You want to split your request between these two servers and get the minimum overall time you need to now 
How much each request would takes.


If we split these files with a round robin algorithm between server A and server B, the biggest wait time is 53 second.it means CDN response the last file after ~60 second (60 sec wait + 1 Sec to process).


	| Order    |FileName|Size(MB)|Server |wait time(Sec)
	|----------|--------|--------|-------|----------
	| 1 	   |F1.mp3  | 2      |A      | 0 
	| 2 	   |F2.mp3  | 50     |B      | 0 
	| 3 	   |F3.mp3  | 4      |A      | 2   (Wating for F1)
	| 4 	   |F4.mp3  | 10     |B      | 50  (Waiting For F2)  	
	| 5 	   |F5.mp3  | 3      |A      | 6   (Wating For F1,F3)
	| 6 	   |F5.mp3  | 1      |B      | 60  (Waiting For F2,F4)

But if we know the file size we can split our request between our servers way more efficient than Round Robin. In this case we only need to wait 19 seconds to start processing all 6 requests but with round robin algorithm we have to wait 60 seconds to start processing all 6 requests.

	| Order    |FileName|Size(MB)|Server |wait time(Sec)
	|----------|--------|--------|-------|----------
	| 1 	   |F1.mp3  | 2      |A      | 0 
	| 2 	   |F2.mp3  | 50     |B      | 0 
	| 3 	   |F3.mp3  | 4      |A      | 2   (Wating for  F1)
	| 4 	   |F4.mp3  | 10     |A      | 6   (Waiting For F1,F3)  	
	| 5 	   |F5.mp3  | 3      |A      | 16  (Wating For F1,F3)
	| 6 	   |F5.mp3  | 1      |A      | 19  (Waiting For F2,F4)


This senario was only one advantage of file size predicion.if you know how big is your file you can figire out when and where you should cache it on your memory server for further requests. Also you can make you load balencing system so smarter, because with this system you know how much time and process will take each request. Based on this information you can make a really fast an efficient load balencing system.(specially for CDN that only metric is file size.) 





