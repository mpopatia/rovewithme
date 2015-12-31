# a simple file formatter
f = open('airports.txt', 'r')

out = open('new.txt', 'w')

for line in f:
     if line == "":
         break
    
     li = line[11:]
     
     l = li.split("</td><td>") 
    
     lastlen = len(l[-1])
     l[-1] = l[-1][:(lastlen-11)]
     
     total = len(l)
    
     code = l[total-1]
     state = l[total-2]
     city = l[total-3]
     nameL = l[0:(total-3)]
     name = " ".join(nameL)

     out.write(name +","+ city +","+ state +","+ code + "\n")
 







