var j = "5 9 2 8\n9 4 7 3\n3 8 6 5";

j.split("\n").map(function(l){let d=l.split(/\s+/).map(n=>parseInt(n,10)),r;for(let i=1;i<d.length;i++){for(let k=0;k<i;k++){if(!(d[i]%d[k])){r=d[i]/d[k];break}if(!(d[k]%d[i])){r=d[k]/d[i];break}}}return r}).reduce((s,v)=>s+v,0);
