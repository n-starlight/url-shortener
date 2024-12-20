

Let's now observe latency values at various thresholds to identify any bottlenecks ,overall performance ,average performance in terms of time duration of request processing !

For post request 10vus for a duration of 10s
![image](https://github.com/user-attachments/assets/0ea84548-d565-4a3a-89bf-e13d358f6abf)
http_req_duration..............: avg=38.63ms  min=7.09ms med=31.81ms  max=218.94ms p(50)=31.81ms  p(90)=53.48ms  p(95)=98.36ms  p(99)=195.79ms
    { expected_response:true }...: avg=38.63ms  min=7.09ms med=31.81ms  max=218.94ms p(50)=31.81ms  p(90)=53.48ms  p(95)=98.36ms  p(99)=195.79ms
http_req_failed................: 0.00%   0 out of 100

We will focus on the http_req_duration for overall performance
1) So on an average request-response total time is 31.81ms (half of requests processed in time less than or equal to ~32 ms)
2) Most requests(90%(90/100) of requests took ~54ms or less,for 80% rise in requests from 50 to 90,processing time increment is ~68% which is okay)
3) 95% requests took ~ 98ms or less (For 5.5% rise in requests from 90 to 95, req. duration increment time is ~8%)
4) 99% requests took ~ 195 ms or less(for further 4.2% rise in requests from 95 to 99, request process time increment is 98% which is huge for only 4 more requests )
5) Last request as total requests 100 took max=218.94ms

For get request
![image](https://github.com/user-attachments/assets/088ab68e-3159-45f6-b15b-06564a7a9c05)


For get request , sleep(0.1s instead of 1s)

![image](https://github.com/user-attachments/assets/b3f6529b-b04f-41e0-9c65-e835a2805e1f)




Test duration 10s -- 
Assumption 1 req takes minimal amount of time in ms so ignoring that .
For a sleep duration of 1s each user can send 1 request per sec .
For a sleep duration of 0.1s each user can send 10 requests per sec .

Put requests
1) Scale to 60 concurrent api calls(vus) in stages of 1) ramp up  to 10 ,duration -'10s' 2) ramp up to 50 , duration - '10s' 3) ramp up to 60 ,duration '20s' 4) and stay there for '60s' 5) ramp down to 0 in '10s'

![image](https://github.com/user-attachments/assets/a3783664-f6ec-4e3c-adfd-9117af8bf2eb)

2) Scale to 100 concurrent api calls(vus) in stages of 1) ramp up  to 10 ,duration -'10s' 2) ramp up to 50 , duration - '10s' 3) ramp up to 100 ,duration '40s'  4) ramp down to 0 in '10s'
![image](https://github.com/user-attachments/assets/37983e65-9742-40c1-9964-547c7cd216bf)

3)Scale to 100 vus in 1) { duration: '80s', target: 100 }, 2) ramp down to 0 in 10s
![image](https://github.com/user-attachments/assets/3289edbc-6136-450e-97f2-139e0437bf8e)

Duration of 1min 20s is sufficient for scaling to 100 vus .

4)   { duration: '2m', target: 100 },{ duration: '5m', target: 200 },{ duration: '10s', target: 0 }
![image](https://github.com/user-attachments/assets/0316ea8e-2315-423b-a7df-fcfa0ef1482b)

requests start getting timed out even for this many concurrent calls with specified durations { duration: '3m', target: 100 },{ duration: '12m', target: 150 },  { duration: '10s', target: 0 }, 



Get requests
2)
![image](https://github.com/user-attachments/assets/d78c6f76-2d5e-4468-b644-18ab09eb7081)





   
   

