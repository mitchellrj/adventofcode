var j = "5 1 9 5\n7 5 3\n2 4 6 8";

j.split("\n").map(l=>l.split(/\s+/).map(n=>parseInt(n,10)).reduce((s,v)=>[Math.min(s[0],v),Math.max(s[1],v)],[Infinity,-Infinity])).reduce((s,v)=>s+(v[1]-v[0]),0);
