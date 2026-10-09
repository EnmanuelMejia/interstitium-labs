/* il-algo-viz.js — animated inline AI algorithm visualizations (vanilla SVG, dark mode).
   Mounts on <figure class="aav" data-algo="slug"></figure>. One shared rAF ticker,
   IntersectionObserver pauses offscreen figures, honors prefers-reduced-motion. */
(function(){
'use strict';
var NS='http://www.w3.org/2000/svg';
var C={grid:'rgba(148,163,184,.10)',axis:'rgba(148,163,184,.32)',text:'#cbd5e1',dim:'#7d8aa0',
 cyan:'#22d3ee',violet:'#a78bfa',gold:'#fbbf24',emerald:'#34d399',rose:'#fb7185',
 orange:'#fb923c',blue:'#60a5fa',pink:'#f472b6'};
function E(t,a,p){var n=document.createElementNS(NS,t);for(var k in a)n.setAttribute(k,a[k]);if(p)p.appendChild(n);return n;}
function mulberry(s){var a=s>>>0;return function(){a|=0;a=a+0x6D2B79F5|0;var t=Math.imul(a^a>>>15,1|a);t=t+Math.imul(t^t>>>7,61|t)^t;return((t^t>>>14)>>>0)/4294967296;};}
function hash(s){var h=2166136261;for(var i=0;i<s.length;i++){h^=s.charCodeAt(i);h=Math.imul(h,16777619);}return h>>>0;}
function label(g,x,y,s,fill,size,anchor){var n=E('text',{x:x,y:y,'font-size':size||10,fill:fill||C.dim,'text-anchor':anchor||'start','font-family':'ui-monospace,SFMono-Regular,Menlo,monospace'},g);n.textContent=s;return n;}
function grid(g,W,H,st){st=st||30;for(var x=st;x<W;x+=st)E('line',{x1:x,y1:0,x2:x,y2:H,stroke:C.grid,'stroke-width':1},g);for(var y=st;y<H;y+=st)E('line',{x1:0,y1:y,x2:W,y2:y,stroke:C.grid,'stroke-width':1},g);}
function ease(k){return k<.5?2*k*k:1-Math.pow(-2*k+2,2)/2;}
function gauss(r,mu,sig){var u=0,v=0;while(!u)u=r();while(!v)v=r();return mu+sig*Math.sqrt(-2*Math.log(u))*Math.cos(2*Math.PI*v);}

var META={
'linear-regression':['Linear Regression','Ordinary least squares fits the line that minimizes total squared error.'],
'logistic-regression':['Logistic Regression','The sigmoid squashes a linear score into a probability for binary outcomes.'],
'decision-tree':['Decision Tree','Greedy splits partition feature space into pure leaf regions.'],
'random-forest':['Random Forest','Bagged trees vote; the majority class wins. Variance drops, bias stays low.'],
'svm':['Support Vector Machine','The max-margin hyperplane — only the support vectors define the boundary.'],
'knn':['k-Nearest Neighbors','A new point takes the majority label of its k closest neighbors.'],
'naive-bayes':['Naive Bayes','Bayes rule with a feature-independence assumption; the higher posterior wins.'],
'gradient-boosting':['Gradient Boosting','Each weak learner fits the residual errors of the ensemble so far.'],
'adaboost':['AdaBoost','Misclassified points gain weight each round so the next stump focuses on them.'],
'xgboost':['XGBoost','Second-order gradient boosting with regularization and pruning for speed and accuracy.'],
'k-means':['k-Means Clustering','Alternate: assign points to the nearest centroid, then move centroids to the mean.'],
'hierarchical-clustering':['Hierarchical Clustering','Agglomerative merging builds a dendrogram from singletons to one cluster.'],
'dbscan':['DBSCAN','Core points chain together through dense neighborhoods; sparse points stay noise.'],
'pca':['Principal Component Analysis','Rotate to the axes of maximum variance, then project onto the top components.'],
'tsne':['t-SNE','Neighborhood probabilities in high dimensions are matched in a 2-D embedding.'],
'actor-critic':['Actor-Critic','The actor picks actions; the critic judges them and the advantage steers the actor.'],
'gaussian-mixture':['Gaussian Mixture Model','Soft clustering: each point belongs to every Gaussian with some responsibility.'],
'policy-gradient':['Policy Gradient','Roll out trajectories, then nudge the policy toward higher-reward behavior.'],
'sarsa':['SARSA','On-policy TD: update Q(s,a) from the action actually taken next.'],
'q-learning':['Q-Learning','Off-policy TD: bootstrap toward the best next action regardless of behavior.'],
'transformer':['Transformer','Self-attention lets every token weigh every other token in parallel.'],
'lstm':['Long Short-Term Memory','Gates guard a persistent cell state, curing the vanishing gradient.'],
'rnn':['Recurrent Neural Network','The hidden state carries memory forward one timestep at a time.'],
'cnn':['Convolutional Neural Network','Learned filters slide over the image, building spatial feature maps.'],
'ann':['Artificial Neural Network','Weighted sums through nonlinearities; signals flow forward, errors flow back.'],
'genetic-algorithms':['Genetic Algorithms','Select the fittest, crossover and mutate — evolution as optimization.'],
'markov-decision-process':['Markov Decision Process','States, actions, transition probabilities and rewards define sequential decisions.'],
'isolation-forest':['Isolation Forest','Anomalies isolate in few random splits; normal points need many.'],
'autoencoders':['Autoencoders','Compress through a bottleneck, then reconstruct — the bottleneck learns the essence.']
};

/* ---- step pills: 3 numbered steps per algorithm, highlighted in sync with the animation cycle ---- */
var STEPS={
'linear-regression':['Scatter the data points','Fit a candidate line','Minimize the squared error'],
'logistic-regression':['Plot the two classes','Draw the sigmoid curve','Threshold at p = 0.5 to classify'],
'decision-tree':['Ask the root question: x1 <= 4.2?','Split again on x2 and x3','Reach a pure leaf: class A or B'],
'random-forest':['Grow three bagged trees','Each tree casts its vote','The majority class wins'],
'svm':['Plot the two classes','Swing the max-margin hyperplane','Support vectors pin the margin'],
'knn':['Plot the labeled points','The query point looks outward','Vote of the k = 1, 3, 5 neighbors'],
'naive-bayes':['Fit the P(x|A) and P(x|B) curves','Slide the evidence marker','The higher posterior wins'],
'gradient-boosting':['Fit a first weak learner','Each round fits the residuals','Residual error shrinks every round'],
'adaboost':['Train a stump classifier','Grow the misclassified points','The next round focuses on the hard ones'],
'xgboost':['Train trees in parallel','Prune the weak splits','Train loss converges'],
'k-means':['Drop three random centroids','Assign points to the nearest','Move centroids to the mean - repeat'],
'hierarchical-clustering':['Start with eight singletons','Merge the closest pairs','One cluster: dendrogram complete'],
'dbscan':['Scan each neighborhood radius','Chain core points into clusters','Sparse points stay noise'],
'pca':['Find the max-variance axes','Rotate onto PC1 and PC2','Project the points onto PC1'],
'tsne':['Start from a high-dim scatter','Match neighborhoods in 2-D','Clusters separate, then relax'],
'actor-critic':['Actor takes action a in state s','Critic scores the reward r','Advantage steers the actor'],
'gaussian-mixture':['Place two Gaussian components','Compute soft responsibilities','Components breathe and settle'],
'policy-gradient':['Roll out a trajectory','Tally the episode reward','Reinforce the high-reward paths'],
'sarsa':['Act in the grid world','Observe reward and next action','Update Q(s,a) from the next action - on-policy'],
'q-learning':['Explore the grid','Check the best next Q value','Bootstrap toward the max - off-policy'],
'transformer':['Embed the tokens','Each head attends token-to-token','The heads combine their views'],
'lstm':['Forget gate drops stale memory','Input gate writes to the cell','Output gate reads out the hidden state'],
'rnn':['Feed in the next token','Update the hidden state','Carry the memory forward in time'],
'cnn':['Slide the kernel over pixels','Convolve into activations','The feature map fills in'],
'ann':['Compute the weighted sums','Push through nonlinearities','Signals reach the output layer'],
'genetic-algorithms':['Rank the population by fitness','Select and cross over the fittest','Mutate into a new generation'],
'markov-decision-process':['Observe the current state','Transition with probability p','Collect reward r - repeat'],
'isolation-forest':['Cut features at random','The anomaly isolates in 2 splits','Short path means outlier'],
'autoencoders':['Encode the input','Squeeze through the bottleneck','Decode and reconstruct the output']
};
/* fraction of each animation cycle where step 2 and step 3 become active */
var STEP_CUT={
'linear-regression':[.15,.55],'logistic-regression':[.15,.5],'decision-tree':[.12,.48],
'random-forest':[.45,.7],'svm':[.33,.67],'knn':[.33,.67],
'naive-bayes':[.25,.75],'gradient-boosting':[.25,.75],'adaboost':[.33,.67],
'xgboost':[.33,.67],'k-means':[.25,.5],'hierarchical-clustering':[.15,.8],
'dbscan':[.4,.75],'pca':[.35,.6],'tsne':[.44,.62],
'actor-critic':[.3,.6],'gaussian-mixture':[.33,.67],'policy-gradient':[.33,.6],
'sarsa':[.4,.7],'q-learning':[.35,.65],'transformer':[.2,.85],
'lstm':[.3,.6],'rnn':[.25,.5],'cnn':[.3,.7],
'ann':[.33,.67],'genetic-algorithms':[.3,.65],'markov-decision-process':[.3,.65],
'isolation-forest':[.35,.6],'autoencoders':[.4,.6]
};
/* animation cycle length (seconds) each viz loops over; continuous viz use a pseudo-cycle */
var STEP_CYCLE={
'linear-regression':6,'logistic-regression':6,'decision-tree':5,
'random-forest':6,'svm':8,'knn':7,
'naive-bayes':6,'gradient-boosting':8,'adaboost':7.5,
'xgboost':6,'k-means':4.8,'hierarchical-clustering':8,
'dbscan':6,'pca':7,'tsne':8,
'actor-critic':6,'gaussian-mixture':6,'policy-gradient':7,
'sarsa':6,'q-learning':8,'transformer':6,
'lstm':5,'rnn':4,'cnn':7,
'ann':6,'genetic-algorithms':8,'markov-decision-process':7.5,
'isolation-forest':7,'autoencoders':4
};

var VIZ={};

/* ---------- 1. Linear Regression ---------- */
VIZ['linear-regression']=function(g,W,H,R){
 grid(g,W,H);
 var pts=[],i;
 for(i=0;i<26;i++){var x=30+R()*300;var y=170-((x-30)/300)*110+(R()-.5)*44;pts.push([x,y]);E('circle',{cx:x,cy:y,r:3,fill:C.cyan,opacity:.75},g);}
 E('line',{x1:20,y1:190,x2:340,y2:190,stroke:C.axis,'stroke-width':1},g);
 E('line',{x1:20,y1:10,x2:20,y2:190,stroke:C.axis,'stroke-width':1},g);
 var line=E('line',{x1:20,y1:170,x2:340,y2:170,stroke:C.gold,'stroke-width':2.5},g);
 var mse=label(g,250,24,'',C.gold,10,'start');
 return function(t){
  var cyc=(t%6)/6, k=cyc<.55?ease(cyc/.55):1;
  var y1=170+(170-170)*k, y2=170+(60-170)*k;
  line.setAttribute('y1',y1);line.setAttribute('y2',y2);
  mse.textContent='MSE '+(0.42+(1-k)*2.1).toFixed(2);
 };
};
/* ---------- 2. Logistic Regression ---------- */
VIZ['logistic-regression']=function(g,W,H,R){
 grid(g,W,H);
 var d='M20,0 ';var path='';
 for(var x=20;x<=340;x+=6){var y=180-150/(1+Math.exp(-(x-180)/26));path+=(x===20?'M':'L')+x.toFixed(1)+','+y.toFixed(1)+' ';}
 var p=E('path',{d:path,fill:'none',stroke:C.violet,'stroke-width':2.5},g);
 var L=p.getTotalLength();p.style.strokeDasharray=L;p.style.strokeDashoffset=L;
 var i,x,y;
 for(i=0;i<14;i++){x=40+R()*110;y=150+R()*30;E('circle',{cx:x,cy:y,r:3.4,fill:C.cyan,opacity:.8},g);}
 for(i=0;i<14;i++){x=210+R()*110;y=30+R()*36;E('circle',{cx:x,cy:y,r:3.4,fill:C.rose,opacity:.8},g);}
 E('line',{x1:20,y1:105,x2:340,y2:105,stroke:C.dim,'stroke-width':1,'stroke-dasharray':'6 5'},g);
 label(g,330,100,'p=0.5',C.dim,9,'end');
 label(g,24,200,'sigmoid σ(z)',C.violet,10);
 return function(t){var cyc=(t%6)/6,k=cyc<.5?ease(cyc/.5):1;p.style.strokeDashoffset=L*(1-k);};
};
/* ---------- 3. Decision Tree ---------- */
VIZ['decision-tree']=function(g,W,H,R){
 grid(g,W,H);
 var nodes=[[180,34,'x₁ ≤ 4.2?'],[100,92,'x₂ ≤ 1.7?'],[260,92,'x₃ ≤ 0.9?'],[58,158,'✓ A'],[142,158,'✗ B'],[218,158,'✓ A'],[302,158,'✗ B']];
 var edges=[[0,1],[0,2],[1,3],[1,4],[2,5],[2,6]];
 var edgeEls=edges.map(function(e){var a=nodes[e[0]],b=nodes[e[1]];
  var l=E('line',{x1:a[0],y1:a[1]+12,x2:b[0],y2:b[1]-12,stroke:C.blue,'stroke-width':1.6},g);
  var L=Math.hypot(b[0]-a[0],b[1]-a[1]-24);l.style.strokeDasharray=L;l.style.strokeDashoffset=L;return l;});
 var nodeEls=nodes.map(function(n,i){var grp=E('g',{},g);
  E('circle',{cx:n[0],cy:n[1],r:i<3?15:13,fill:i<3?'#101a30':'#0d1626',stroke:i<3?C.blue:C.emerald,'stroke-width':2},grp);
  label(grp,n[0],n[1]+(i<3?4:5),n[2],i<3?C.text:(n[2][0]==='✓'?C.emerald:C.rose),i<3?8.5:10,'middle');
  grp.style.opacity=0;return grp;});
 return function(t){var cyc=t%5;
  edgeEls.forEach(function(l,i){var L=parseFloat(l.style.strokeDasharray);var k=Math.max(0,Math.min(1,(cyc-0.3-i*0.45)/0.6));l.style.strokeDashoffset=L*(1-ease(k));});
  nodeEls.forEach(function(n,i){var k=Math.max(0,Math.min(1,(cyc-i*0.5)/0.4));n.style.opacity=k;});
 };
};
/* ---------- 4. Random Forest ---------- */
VIZ['random-forest']=function(g,W,H,R){
 grid(g,W,H);
 var trees=[[70],[180],[290]],votes=['A','A','B'],cols=[C.cyan,C.cyan,C.rose];
 var els=trees.map(function(tx,i){var grp=E('g',{},g);
  E('circle',{cx:tx[0],cy:50,r:13,fill:'#101a30',stroke:C.blue,'stroke-width':2},grp);
  E('line',{x1:tx[0]-6,y1:62,x2:tx[0]-22,y2:96,stroke:C.blue,'stroke-width':1.5},grp);
  E('line',{x1:tx[0]+6,y1:62,x2:tx[0]+22,y2:96,stroke:C.blue,'stroke-width':1.5},grp);
  E('circle',{cx:tx[0]-26,cy:104,r:11,fill:'#0d1626',stroke:cols[i],'stroke-width':2},grp);
  E('circle',{cx:tx[0]+26,cy:104,r:11,fill:'#0d1626',stroke:cols[i],'stroke-width':2},grp);
  var v=label(grp,tx[0],150,'vote: '+votes[i],cols[i],11,'middle');v.style.opacity=0;
  grp.style.opacity=0;return{grp:grp,vote:v};});
 var tally=label(g,180,178,'tally  A:0  B:0',C.text,12,'middle');
 var win=label(g,180,202,'',C.gold,13,'middle');win.setAttribute('font-weight','bold');
 return function(t){var cyc=t%6;
  els.forEach(function(e,i){var k=Math.max(0,Math.min(1,(cyc-i*1.1)/0.7));e.grp.style.opacity=k;
   e.vote.style.opacity=Math.max(0,Math.min(1,(cyc-i*1.1-0.6)/0.4));});
  var shown=Math.min(3,Math.floor(Math.max(0,cyc-0.6)/1.1)+ (cyc>0.6?1:0));
  var a=0,b=0;for(var i=0;i<shown;i++){if(votes[i]==='A')a++;else b++;}
  tally.textContent='tally  A:'+a+'  B:'+b;
  win.textContent=cyc>4.2?'majority → class A wins':'';
 };
};
/* ---------- 5. SVM ---------- */
VIZ['svm']=function(g,W,H,R){
 grid(g,W,H);
 var i,x,y;
 for(i=0;i<14;i++){x=40+R()*90;y=120+R()*55;E('circle',{cx:x,cy:y,r:3.6,fill:C.cyan,opacity:.8},g);}
 for(i=0;i<14;i++){x=220+R()*90;y=25+R()*55;E('circle',{cx:x,cy:y,r:3.6,fill:C.rose,opacity:.8},g);}
 var sv=[[128,138],[228,66]];
 var rings=sv.map(function(p){return E('circle',{cx:p[0],cy:p[1],r:7,fill:'none',stroke:C.gold,'stroke-width':1.6},g);});
 var hyp=E('line',{stroke:C.gold,'stroke-width':2.5},g);
 var m1=E('line',{stroke:C.dim,'stroke-width':1,'stroke-dasharray':'6 5'},g);
 var m2=E('line',{stroke:C.dim,'stroke-width':1,'stroke-dasharray':'6 5'},g);
 label(g,24,200,'max-margin boundary',C.gold,10);
 return function(t){
  var wob=Math.sin(t*1.4)*0.05, ang=-0.62+wob;
  var cx=180,cy=102,dx=Math.cos(ang),dy=Math.sin(ang),L=190;
  hyp.setAttribute('x1',cx-dx*L);hyp.setAttribute('y1',cy-dy*L);
  hyp.setAttribute('x2',cx+dx*L);hyp.setAttribute('y2',cy+dy*L);
  var nx=-dy,ny=dx,off=34;
  m1.setAttribute('x1',cx-dx*L+nx*off);m1.setAttribute('y1',cy-dy*L+ny*off);
  m1.setAttribute('x2',cx+dx*L+nx*off);m1.setAttribute('y2',cy+dy*L+ny*off);
  m2.setAttribute('x1',cx-dx*L-nx*off);m2.setAttribute('y1',cy-dy*L-ny*off);
  m2.setAttribute('x2',cx+dx*L-nx*off);m2.setAttribute('y2',cy+dy*L-ny*off);
  rings.forEach(function(r,i){r.setAttribute('r',7+2.5*Math.sin(t*3+i*2));});
 };
};
/* ---------- 6. k-NN ---------- */
VIZ['knn']=function(g,W,H,R){
 grid(g,W,H);
 var pts=[],i,x,y;
 for(i=0;i<26;i++){x=30+R()*300;y=20+R()*180;var c=(x<180?R()<.8:R()<.2)?C.cyan:C.rose;pts.push(E('circle',{cx:x,cy:y,r:3.4,fill:c,opacity:.7},g));}
 var qx=180,qy=100;
 var star=E('path',{d:'M180,88 l3.5,7 7.6.6 -5.8,5 1.7,7.4 -6.9-3.9 -7,3.9 1.8-7.4 -5.8-5 7.6-.6z',fill:C.gold,stroke:'#7c5a10','stroke-width':1},g);
 label(g,qx,qy+26,'query',C.gold,9,'middle');
 var ring=E('circle',{cx:qx,cy:qy,r:10,fill:'none',stroke:C.gold,'stroke-width':1.5,opacity:.8},g);
 var out=label(g,180,206,'',C.text,11,'middle');
 var dists=pts.map(function(p){var dx=+p.getAttribute('cx')-qx,dy=+p.getAttribute('cy')-qy;return[Math.hypot(dx,dy),p];}).sort(function(a,b){return a[0]-b[0];});
 return function(t){var cyc=t%7,ks=[1,3,5],ki=Math.floor(cyc/2.33)%3,k=ks[ki];
  ring.setAttribute('r',10+((t*40)%(dists[k-1][0]+14)));
  dists.forEach(function(d,i){d[1].setAttribute('r',i<k?5.5:3.4);d[1].setAttribute('stroke',i<k?C.gold:'none');d[1].setAttribute('stroke-width',i<k?1.6:0);});
  var a=0;for(var i=0;i<k;i++){if(dists[i][1].getAttribute('fill')===C.cyan)a++;}
  out.textContent='k='+k+' → '+(a>k/2?'● cyan ('+a+'/'+k+')':'● rose ('+(k-a)+'/'+k+')');
 };
};
/* ---------- 7. Naive Bayes ---------- */
VIZ['naive-bayes']=function(g,W,H,R){
 grid(g,W,H);
 function gpath(mu,sig,col){var d='';for(var x=20;x<=340;x+=4){var y=170-120*Math.exp(-((x-mu)*(x-mu))/(2*sig*sig));d+=(x===20?'M':'L')+x+','+y.toFixed(1)+' ';}return E('path',{d:d,fill:'none',stroke:col,'stroke-width':2.5},g);}
 gpath(130,42,C.cyan);gpath(230,42,C.rose);
 label(g,130,196,'P(x|A)',C.cyan,10,'middle');label(g,230,196,'P(x|B)',C.rose,10,'middle');
 var marker=E('line',{x1:180,y1:20,x2:180,y2:180,stroke:C.gold,'stroke-width':2},g);
 var tri=E('path',{d:'M180,14 l7,12 h-14 z',fill:C.gold},g);
 var barA=E('rect',{x:30,y:30,width:0,height:10,fill:C.cyan,rx:3},g);
 var barB=E('rect',{x:30,y:46,width:0,height:10,fill:C.rose,rx:3},g);
 label(g,24,38,'P(A|x)',C.text,9);label(g,24,54,'P(B|x)',C.text,9);
 return function(t){var cyc=t%6,seg=Math.floor(cyc/2)%3,mx=[100,180,260][seg];
  marker.setAttribute('x1',mx);marker.setAttribute('x2',mx);tri.setAttribute('transform','translate('+(mx-180)+',0)');
  var la=Math.exp(-((mx-130)*(mx-130))/(2*42*42)),lb=Math.exp(-((mx-230)*(mx-230))/(2*42*42)),s=la+lb;
  barA.setAttribute('width',120*la/s);barB.setAttribute('width',120*lb/s);
 };
};
/* ---------- 8. Gradient Boosting ---------- */
VIZ['gradient-boosting']=function(g,W,H,R){
 grid(g,W,H);
 label(g,24,20,'residual error per round',C.text,10);
 var bars=[],i;
 for(i=0;i<6;i++){bars.push(E('rect',{x:40+i*48,y:60,width:30,height:100,fill:C.rose,opacity:.8,rx:3},g));}
 var round=label(g,320,30,'round 1/4',C.gold,11,'end');
 var stumps=[];
 return function(t){var cyc=t%8,r=Math.min(4,1+Math.floor(cyc/2));
  round.textContent='round '+r+'/4';
  var shrink=Math.pow(0.55,r-1);
  bars.forEach(function(b,i){var h=100*shrink*(0.7+0.6*((i*37)%10)/10);b.setAttribute('height',h);b.setAttribute('y',160-h);});
  while(stumps.length<r){var n=stumps.length;
   stumps.push(E('line',{x1:30,y1:150-n*22,x2:330,y2:150-n*22,stroke:C.cyan,'stroke-width':1.6,'stroke-dasharray':'7 4',opacity:.85},g));}
  stumps.forEach(function(s,i){s.style.opacity=i<r?0.85:0;});
 };
};
/* ---------- 9. AdaBoost ---------- */
VIZ['adaboost']=function(g,W,H,R){
 grid(g,W,H);
 var pts=[],i,x,y,miss=[3,9];
 for(i=0;i<12;i++){x=40+(i%6)*52;y=60+Math.floor(i/6)*70;
  var c=(i%6<3)?C.cyan:C.rose;
  pts.push({el:E('circle',{cx:x,cy:y,r:6,fill:c,opacity:.85},g),miss:miss.indexOf(i)>=0});}
 var stump=E('line',{x1:190,y1:30,x2:190,y2:170,stroke:C.gold,'stroke-width':2},g);
 var rd=label(g,320,24,'round 1/3',C.gold,11,'end');
 return function(t){var cyc=t%7.5,r=Math.min(3,1+Math.floor(cyc/2.5));
  rd.textContent='round '+r+'/3';
  pts.forEach(function(p,i){var w=p.miss?6+3.2*(r-1):Math.max(2.5,6-1.8*(r-1));
   p.el.setAttribute('r',w);p.el.setAttribute('stroke',p.miss?C.gold:'none');p.el.setAttribute('stroke-width',1.5);});
  stump.setAttribute('x1',190+(r-2)*36);stump.setAttribute('x2',190+(r-2)*36);
 };
};
/* ---------- 10. XGBoost ---------- */
VIZ['xgboost']=function(g,W,H,R){
 grid(g,W,H);
 var d='M30,170 ';var pts=[[30,170],[90,140],[150,100],[210,62],[270,40],[330,30]];
 pts.forEach(function(p){d+='L'+p[0]+','+p[1]+' ';});
 var curve=E('path',{d:d,fill:'none',stroke:C.emerald,'stroke-width':2.5},g);
 var L=curve.getTotalLength();curve.style.strokeDasharray=L;curve.style.strokeDashoffset=L;
 label(g,24,200,'train loss ↓',C.emerald,10);
 for(var i=0;i<8;i++){E('rect',{x:36+i*38,y:196,width:22,height:8,fill:C.violet,opacity:.25,rx:2},g);}
 var workers=g;
 var wb=[];for(i=0;i<8;i++){wb.push(E('rect',{x:36+i*38,y:196,width:22,height:8,fill:C.violet,opacity:.9,rx:2},g));}
 var pruned=E('g',{opacity:0},g);
 E('line',{x1:250,y1:60,x2:290,y2:100,stroke:C.dim,'stroke-width':1.5},pruned);
 E('line',{x1:250,y1:60,x2:210,y2:100,stroke:C.dim,'stroke-width':1.5},pruned);
 label(pruned,250,52,'pruned ✕',C.rose,9,'middle');
 label(g,320,24,'parallel trees',C.violet,10,'end');
 return function(t){var cyc=t%6,k=cyc<3?ease(cyc/3):1;
  curve.style.strokeDashoffset=L*(1-k);
  wb.forEach(function(b,i){b.style.opacity=i/8<k?0.9:0.15;});
  pruned.style.opacity=cyc>4?Math.min(1,(cyc-4)):0;
 };
};
/* ---------- 11. k-Means ---------- */
VIZ['k-means']=function(g,W,H,R){
 grid(g,W,H);
 var centers=[[90,70],[270,70],[180,165]],cols=[C.cyan,C.rose,C.gold];
 var pts=[],i,c,x,y;
 for(c=0;c<3;c++)for(i=0;i<12;i++){x=centers[c][0]+gauss(R,0,26);y=centers[c][1]+gauss(R,0,20);
  pts.push({el:E('circle',{cx:x,cy:y,r:3.4,fill:cols[c],opacity:.8},g),x:x,y:y,a:c});}
 var marks=centers.map(function(cc,i){var m=E('g',{},g);
  E('line',{x1:cc[0]-7,y1:cc[1]-7,x2:cc[0]+7,y2:cc[1]+7,stroke:'#fff','stroke-width':2.5},m);
  E('line',{x1:cc[0]-7,y1:cc[1]+7,x2:cc[0]+7,y2:cc[1]-7,stroke:'#fff','stroke-width':2.5},m);return m;});
 var it=label(g,320,24,'iter 0',C.text,10,'end');
 var step=0;
 function reassign(){var sums=[[0,0,0],[0,0,0],[0,0,0]];
  pts.forEach(function(p){var best=0,bd=1e9;
   centers.forEach(function(cc,i){var d=(p.x-cc[0])*(p.x-cc[0])+(p.y-cc[1])*(p.y-cc[1]);if(d<bd){bd=d;best=i;}});
   p.a=best;p.el.setAttribute('fill',cols[best]);sums[best][0]+=p.x;sums[best][1]+=p.y;sums[best][2]++;});
  centers.forEach(function(cc,i){if(sums[i][2]){cc[0]=sums[i][0]/sums[i][2];cc[1]=sums[i][1]/sums[i][2];}});
  step++;it.textContent='iter '+step;}
 reassign();reassign();
 var lastStep=0;
 return function(t){var s=Math.floor(t/1.6);
  if(s!==lastStep){lastStep=s;reassign();}
  centers.forEach(function(cc,i){var m=marks[i].childNodes;
   m[0].setAttribute('x1',cc[0]-7);m[0].setAttribute('y1',cc[1]-7);m[0].setAttribute('x2',cc[0]+7);m[0].setAttribute('y2',cc[1]+7);
   m[1].setAttribute('x1',cc[0]-7);m[1].setAttribute('y1',cc[1]+7);m[1].setAttribute('x2',cc[0]+7);m[1].setAttribute('y2',cc[1]-7);});
 };
};
/* ---------- 12. Hierarchical Clustering ---------- */
VIZ['hierarchical-clustering']=function(g,W,H,R){
 grid(g,W,H);
 var n=8,xs=[],i;
 for(i=0;i<n;i++){xs.push(40+i*40);E('circle',{cx:40+i*40,cy:196,r:4,fill:C.cyan,opacity:.85},g);}
 function link(x1,x2,y){var my=y-26;
  var p=E('path',{d:'M'+x1+',196 L'+x1+','+my+' L'+x2+','+my+' L'+x2+',196',fill:'none',stroke:C.violet,'stroke-width':1.8},g);
  var L=p.getTotalLength();p.style.strokeDasharray=L;p.style.strokeDashoffset=L;return{p:p,L:L,mx:(x1+x2)/2,my:my};}
 var merges=[],pairs=[[0,1],[2,3],[4,5],[6,7],[40,120],[200,280],[80,240]];
 var ys=[0,0,0,0,1,1,2];
 pairs.forEach(function(pr,j){var x1=pr[0]<8?xs[pr[0]]:pr[0],x2=pr[1]<8?xs[pr[1]]:pr[1];
  merges.push(link(x1,x2,196-ys[j]*0));});
 label(g,24,24,'agglomerative merging →',C.violet,10);
 var top=E('circle',{cx:180,cy:34,r:5,fill:C.gold,opacity:0},g);
 return function(t){var cyc=t%8;
  merges.forEach(function(m,i){var k=Math.max(0,Math.min(1,(cyc-0.4-i*0.85)/0.7));
   m.p.style.strokeDashoffset=m.L*(1-ease(k));});
  top.style.opacity=cyc>6.6?Math.min(1,cyc-6.6):0;
 };
};
/* ---------- 13. DBSCAN ---------- */
VIZ['dbscan']=function(g,W,H,R){
 grid(g,W,H);
 var pts=[],i,x,y;
 var blobs=[[110,90,26],[250,120,30]];
 blobs.forEach(function(b){for(i=0;i<16;i++){x=b[0]+gauss(R,0,b[2]);y=b[1]+gauss(R,0,b[2]*0.8);
  pts.push({el:E('circle',{cx:x,cy:y,r:3.4,fill:C.dim,opacity:.8},g),x:x,y:y,core:false});}});
 for(i=0;i<5;i++){x=40+R()*280;y=20+R()*180;
  pts.push({el:E('circle',{cx:x,cy:y,r:2.6,fill:'#5b6478',opacity:.7},g),x:x,y:y,noise:true});}
 var eps=46;
 var wave=E('circle',{cx:0,cy:0,r:0,fill:'none',stroke:C.cyan,'stroke-width':1.5,opacity:0},g);
 label(g,24,200,'ε-neighborhood chains core points',C.cyan,10);
 return function(t){var cyc=t%6;
  var visited={},queue=[],found=[];
  function neighbors(p){var out=[];pts.forEach(function(q){if(q===p||q.noise)return;
   if(Math.hypot(p.x-q.x,p.y-q.y)<eps)out.push(q);});return out;}
  var seeds=pts.filter(function(p){return !p.noise;}).slice(0,10);
  seeds.forEach(function(s){var nb=neighbors(s);if(nb.length>=4){s.core=true;nb.forEach(function(q){q.core=true;});}});
  var k=Math.min(1,cyc/3.2);
  pts.forEach(function(p){if(p.noise){p.el.setAttribute('fill','#5b6478');return;}
   p.el.setAttribute('fill',p.core?C.cyan:C.violet);p.el.setAttribute('opacity',p.core?0.4+0.5*k:0.8);});
  var si=Math.floor(cyc*2)%Math.max(1,seeds.length),sp=seeds[si];
  if(sp){wave.setAttribute('cx',sp.x);wave.setAttribute('cy',sp.y);
   wave.setAttribute('r',(cyc*60)%eps);wave.setAttribute('opacity',0.7);}
 };
};
/* ---------- 14. PCA ---------- */
VIZ['pca']=function(g,W,H,R){
 var grp=E('g',{},g);grid(grp,W,H);
 var pts=[],i;
 for(i=0;i<30;i++){var a=R()*Math.PI*2,r=Math.sqrt(R());
  var lx=Math.cos(a)*r*110,ly=Math.sin(a)*r*38;
  var ang=0.5,x=180+lx*Math.cos(ang)-ly*Math.sin(ang),y=105+lx*Math.sin(ang)+ly*Math.cos(ang);
  pts.push({el:E('circle',{cx:x,cy:y,r:3.2,fill:C.blue,opacity:.75},grp),lx:lx,ly:ly});}
 var ax1=E('line',{x1:70,y1:160,x2:290,y2:50,stroke:C.gold,'stroke-width':2},grp);
 var ax2=E('line',{x1:150,y1:30,x2:210,y2:180,stroke:C.dim,'stroke-width':1.2,'stroke-dasharray':'5 4'},grp);
 label(grp,292,48,'PC1',C.gold,10);label(grp,212,184,'PC2',C.dim,10);
 var projs=[];for(i=0;i<5;i++){projs.push(E('line',{stroke:C.gold,'stroke-width':1,opacity:.5,'stroke-dasharray':'3 3'},grp));}
 return function(t){var cyc=t%7,k=cyc<3.5?ease(cyc/3.5):1;
  var rot=0.5*(1-k);
  pts.forEach(function(p){var x=180+p.lx*Math.cos(rot)-p.ly*Math.sin(rot),y=105+p.lx*Math.sin(rot)+p.ly*Math.cos(rot);
   p.el.setAttribute('cx',x);p.el.setAttribute('cy',y);});
  var a1=Math.atan2(50-160,290-70)-0.5*(1-k);
  var dx=Math.cos(a1),dy=Math.sin(a1);
  ax1.setAttribute('x1',180-dx*115);ax1.setAttribute('y1',105-dy*115);
  ax1.setAttribute('x2',180+dx*115);ax1.setAttribute('y2',105+dy*115);
  projs.forEach(function(pr,i){var p=pts[i*6];var px=+p.el.getAttribute('cx'),py=+p.el.getAttribute('cy');
   var t2=((px-180)*dx+(py-105)*dy);var qx=180+dx*t2,qy=105+dy*t2;
   pr.setAttribute('x1',px);pr.setAttribute('y1',py);pr.setAttribute('x2',qx);pr.setAttribute('y2',qy);
   pr.style.opacity=k>0.8?0.6:0;});
 };
};
/* ---------- 15. t-SNE ---------- */
VIZ['tsne']=function(g,W,H,R){
 grid(g,W,H);
 label(g,24,20,'high-dim neighborhoods',C.dim,10);
 label(g,216,20,'2-D embedding',C.emerald,10);
 E('line',{x1:196,y1:60,x2:164,y2:60,stroke:C.axis,'stroke-width':1},g);
 var pts=[],i,cols=[C.cyan,C.rose,C.gold];
 for(i=0;i<24;i++){var c=i%3;
  var sx=60+gauss(R,0,34),sy=110+gauss(R,0,52);
  var tx=258+Math.cos(c*2.1)*34+gauss(R,0,10),ty=110+Math.sin(c*2.1)*38+gauss(R,0,10);
  pts.push({el:E('circle',{cx:sx,cy:sy,r:3.4,fill:cols[c],opacity:.85},g),sx:sx,sy:sy,tx:tx,ty:ty});}
 return function(t){var cyc=t%8,k=cyc<3.5?ease(cyc/3.5):(cyc<5?1:1-ease((cyc-5)/3));
  pts.forEach(function(p){p.el.setAttribute('cx',p.sx+(p.tx-p.sx)*k);p.el.setAttribute('cy',p.sy+(p.ty-p.sy)*k);});
 };
};
/* ---------- 16. Actor-Critic ---------- */
VIZ['actor-critic']=function(g,W,H,R){
 grid(g,W,H);
 function node(x,y,l,col){E('rect',{x:x-44,y:y-20,width:88,height:40,rx:10,fill:'#101a30',stroke:col,'stroke-width':2},g);
  label(g,x,y+4,l,col,11,'middle');}
 node(90,70,'ACTOR',C.cyan);node(270,70,'CRITIC',C.violet);
 E('rect',{x:136,y:150,width:88,height:40,rx:10,fill:'#101a30',stroke:C.dim,'stroke-width':2},g);
 label(g,180,174,'ENV',C.dim,11,'middle');
 var flows=[
  {d:'M134,70 L226,70',l:'state s',c:C.dim},
  {d:'M110,90 Q140,130 158,150',l:'action a',c:C.cyan},
  {d:'M202,150 Q230,130 250,90',l:'reward r',c:C.gold},
  {d:'M226,70 Q180,40 134,70',l:'advantage δ',c:C.violet}];
 var fl=flows.map(function(f){var p=E('path',{d:f.d,fill:'none',stroke:f.c,'stroke-width':1.8,'stroke-dasharray':'7 6',opacity:.35},g);
  label(g,0,0,'',f.c,9);return p;});
 var dots=flows.map(function(f){return E('circle',{r:4,fill:f.c},g);});
 label(g,180,24,'advantage steers the actor',C.violet,10,'middle');
 return function(t){
  flows.forEach(function(f,i){var p=fl[i],L=p.getTotalLength();
   var ph=((t*0.9+i*0.25)%1);
   p.style.strokeDashoffset=-ph*L;
   p.setAttribute('opacity',0.3+0.5*Math.abs(Math.sin(t*2+i)));
   var pt=p.getPointAtLength(ph*L);dots[i].setAttribute('cx',pt.x);dots[i].setAttribute('cy',pt.y);});
 };
};
/* ---------- 17. Gaussian Mixture ---------- */
VIZ['gaussian-mixture']=function(g,W,H,R){
 grid(g,W,H);
 var comps=[{x:130,y:105,rx:62,ry:36,c:C.cyan},{x:235,y:115,rx:58,ry:40,c:C.rose}];
 var ells=comps.map(function(cp){return E('ellipse',{cx:cp.x,cy:cp.y,rx:cp.rx,ry:cp.ry,fill:'none',stroke:cp.c,'stroke-width':1.8,'stroke-dasharray':'8 5',opacity:.8},g);});
 var pts=[],i;
 for(i=0;i<26;i++){var c=i%2,cp=comps[c];
  var x=cp.x+gauss(R,0,cp.rx/2.4),y=cp.y+gauss(R,0,cp.ry/2.4);
  var el=E('circle',{cx:x,cy:y,r:3.2,fill:cp.c,opacity:.55},g);
  pts.push({el:el,x:x,y:y});}
 label(g,24,200,'soft responsibilities — every point, every component',C.dim,10);
 return function(t){
  ells.forEach(function(e,i){e.setAttribute('rx',comps[i].rx+6*Math.sin(t*1.2+i*2));
   e.setAttribute('ry',comps[i].ry+5*Math.cos(t*1.1+i));});
  pts.forEach(function(p,i){p.el.setAttribute('opacity',0.35+0.35*Math.abs(Math.sin(t*1.5+i)));});
 };
};
/* ---------- 18. Policy Gradient ---------- */
VIZ['policy-gradient']=function(g,W,H,R){
 grid(g,W,H);
 var d='M30,170 Q100,150 130,110 T220,90 T330,50';
 E('path',{d:d,fill:'none',stroke:C.axis,'stroke-width':1.5,'stroke-dasharray':'4 5'},g);
 var ghost1=E('path',{d:'M30,170 Q90,170 140,130 T230,110 T330,70',fill:'none',stroke:C.dim,'stroke-width':1.2,opacity:.4},g);
 var best=E('path',{d:d,fill:'none',stroke:C.emerald,'stroke-width':2.5},g);
 var L=best.getTotalLength();best.style.strokeDasharray=L;
 var agent=E('circle',{r:6,fill:C.gold,stroke:'#7c5a10','stroke-width':1.5},g);
 var rw=label(g,320,24,'reward 0',C.gold,11,'end');
 label(g,24,200,'rollout → reinforce high-reward paths',C.emerald,10);
 return function(t){var cyc=t%7,ep=Math.floor(cyc/2.33);
  var k=(cyc%2.33)/2.33;
  best.style.strokeDashoffset=L*(1-Math.min(1,k*1.4));
  var pt=best.getPointAtLength(Math.min(1,k)*L);
  agent.setAttribute('cx',pt.x);agent.setAttribute('cy',pt.y);
  rw.textContent='reward '+(ep*37+Math.floor(k*37));
  ghost1.style.opacity=0.4*(1-ep/3);
 };
};
/* ---------- 19. SARSA ---------- */
VIZ['sarsa']=function(g,W,H,R){
 var s=52,ox=96,oy=30;
 for(var r=0;r<3;r++)for(var c=0;c<3;c++)
  E('rect',{x:ox+c*s,y:oy+r*s,width:s-4,height:s-4,rx:6,fill:'#0d1626',stroke:C.axis,'stroke-width':1},g);
 E('rect',{x:ox+2*s,y:oy+2*s,width:s-4,height:s-4,rx:6,fill:'rgba(52,211,153,.15)',stroke:C.emerald,'stroke-width':2},g);
 label(g,ox+2*s+24,oy+2*s+30,'★',C.emerald,16,'middle');
 var path=[[0,0],[1,0],[1,1],[2,1],[2,2]];
 var ag=E('circle',{r:9,fill:C.cyan,stroke:'#0e7490','stroke-width':2},g);
 var arrows=path.map(function(p,i){if(i===path.length-1)return null;
  var n=path[i+1];var x1=ox+p[0]*s+24,y1=oy+p[1]*s+24,x2=ox+n[0]*s+24,y2=oy+n[1]*s+24;
  var a=E('line',{x1:x1,y1:y1,x2:x2,y2:y2,stroke:C.cyan,'stroke-width':1.6,opacity:.25},g);return a;});
 label(g,180,208,'on-policy: learn from the action actually taken',C.cyan,10,'middle');
 return function(t){var cyc=t%6,idx=Math.min(4,Math.floor(cyc/1.1));
  var p=path[idx];ag.setAttribute('cx',ox+p[0]*s+24);ag.setAttribute('cy',oy+p[1]*s+24);
  arrows.forEach(function(a,i){if(a)a.setAttribute('opacity',i<=idx?0.95:0.2);});
 };
};
/* ---------- 20. Q-Learning ---------- */
VIZ['q-learning']=function(g,W,H,R){
 var s=44,ox=92,oy=26;
 var cells=[];
 for(var r=0;r<4;r++)for(var c=0;c<4;c++){
  E('rect',{x:ox+c*s,y:oy+r*s,width:s-3,height:s-3,rx:5,fill:'#0d1626',stroke:C.axis,'stroke-width':1},g);
  var bar=E('rect',{x:ox+c*s+8,y:oy+r*s+s-12,width:0,height:6,fill:C.violet,rx:2},g);
  cells.push({bar:bar,q:R()*0.3});}
 E('rect',{x:ox+3*s,y:oy+3*s,width:s-3,height:s-3,rx:5,fill:'rgba(251,191,36,.12)',stroke:C.gold,'stroke-width':2},g);
 label(g,ox+3*s+20,oy+3*s+30,'★',C.gold,14,'middle');
 var ag=E('circle',{r:8,fill:C.rose,stroke:'#9f1239','stroke-width':2},g);
 label(g,180,210,'off-policy: bootstrap toward the best next action',C.rose,10,'middle');
 var pos=[0,0];
 return function(t){var cyc=t%8,step=Math.floor(cyc/0.7);
  if(R()<0.12){pos=[Math.floor(R()*4),Math.floor(R()*4)];}
  else{if(pos[0]<3)pos[0]++;else if(pos[1]<3)pos[1]++;}
  cells.forEach(function(cl,i){var cr=Math.floor(i/4),cc=i%4;
   var d=Math.abs(cr-pos[1])+Math.abs(cc-pos[0]);
   cl.q=Math.min(1,cl.q+0.02*(4-d)/4);
   cl.bar.setAttribute('width',(s-16)*cl.q);});
  ag.setAttribute('cx',ox+pos[0]*s+20);ag.setAttribute('cy',oy+pos[1]*s+20);
 };
};
/* ---------- 21. Transformer ---------- */
VIZ['transformer']=function(g,W,H,R){
 grid(g,W,H);
 var toks=['The','cat','sat','down','▮'],n=toks.length,bw=56,gap=14,x0=(W-(n*bw+(n-1)*gap))/2;
 var boxes=toks.map(function(tk,i){var x=x0+i*(bw+gap);
  E('rect',{x:x,y:150,width:bw,height:34,rx:8,fill:'#101a30',stroke:C.blue,'stroke-width':1.8},g);
  label(g,x+bw/2,172,tk,C.text,10,'middle');return x+bw/2;});
 var heads=[C.cyan,C.violet,C.gold],arcs=[];
 for(var h=0;h<3;h++)for(var i=0;i<n;i++)for(var j=i+1;j<n;j++){
  var mx=(boxes[i]+boxes[j])/2,hh=150-24-Math.abs(j-i)*16;
  arcs.push({p:E('path',{d:'M'+boxes[i]+',150 Q'+mx+','+hh+' '+boxes[j]+',150',fill:'none',stroke:heads[h],'stroke-width':1.4,opacity:0},g),h:h});}
 label(g,180,30,'multi-head self-attention',C.blue,11,'middle');
 return function(t){var cyc=t%6,active=Math.floor(cyc/2)%3;
  arcs.forEach(function(a){var on=a.h===active;
   a.p.setAttribute('opacity',on?0.75:0.06);
   if(on)a.p.style.strokeDasharray='6 5',a.p.style.strokeDashoffset=-(t*30)%11;});
 };
};
/* ---------- 22. LSTM ---------- */
VIZ['lstm']=function(g,W,H,R){
 grid(g,W,H);
 E('line',{x1:20,y1:60,x2:340,y2:60,stroke:C.gold,'stroke-width':2.5,opacity:.85},g);
 label(g,24,44,'cell state C',C.gold,10);
 var gates=[['forget',90,C.rose],['input',180,C.cyan],['output',270,C.violet]];
 var valves=gates.map(function(gt){var grp=E('g',{},g);
  E('circle',{cx:gt[1],cy:120,r:22,fill:'#101a30',stroke:gt[2],'stroke-width':2},grp);
  label(grp,gt[1],124,gt[0],gt[2],9,'middle');
  E('line',{x1:gt[1],y1:150,x2:gt[1],y2:60,stroke:gt[2],'stroke-width':1.4,'stroke-dasharray':'4 4',opacity:.7},grp);
  return grp;});
 E('line',{x1:20,y1:120,x2:340,y2:120,stroke:C.axis,'stroke-width':1.5},g);
 label(g,24,140,'xₜ in →',C.dim,10);label(g,300,140,'hₜ out →',C.dim,10);
 var pulse=E('circle',{r:5,fill:'#fff'},g);
 return function(t){var cyc=t%5;
  valves.forEach(function(v,i){var open=0.5+0.5*Math.sin(cyc*2.5+i*2.1);
   v.childNodes[0].setAttribute('r',14+8*open);v.setAttribute('opacity',0.55+0.45*open);});
  var px=20+cyc/5*320;pulse.setAttribute('cx',px);pulse.setAttribute('cy',60);
  pulse.setAttribute('opacity',0.9);
 };
};
/* ---------- 23. RNN ---------- */
VIZ['rnn']=function(g,W,H,R){
 grid(g,W,H);
 var cells=[70,150,230,310],toks=['I','love','AI','▮'];
 var boxes=cells.map(function(x,i){E('rect',{x:x-30,y:80,width:60,height:52,rx:10,fill:'#101a30',stroke:C.cyan,'stroke-width':2},g);
  label(g,x,110,'h'+(i+1),C.cyan,11,'middle');
  label(g,x,170,toks[i],C.dim,10,'middle');
  E('line',{x1:x,y1:150,x2:x,y2:132,stroke:C.dim,'stroke-width':1.4},g);return x;});
 for(var i=0;i<3;i++){E('line',{x1:cells[i]+30,y1:106,x2:cells[i+1]-30,y2:106,stroke:C.cyan,'stroke-width':2},g);
  E('path',{d:'M'+(cells[i+1]-30)+',106 l-8,-4 v8 z',fill:C.cyan},g);}
 label(g,180,36,'hidden state flows forward in time',C.cyan,10,'middle');
 var pulse=E('circle',{r:5,fill:C.gold},g);
 return function(t){var cyc=t%4,seg=Math.min(2.99,cyc),i=Math.floor(seg),k=seg-i;
  var x=cells[i]+30+k*50;pulse.setAttribute('cx',x);pulse.setAttribute('cy',106);};
};
/* ---------- 24. CNN ---------- */
VIZ['cnn']=function(g,W,H,R){
 label(g,24,20,'input',C.dim,10);label(g,216,20,'feature map',C.emerald,10);
 var px=10,pix=[];
 for(var r=0;r<8;r++)for(var c=0;c<8;c++){var v=R();
  pix.push(E('rect',{x:24+c*px,y:30+r*px,width:px-1,height:px-1,fill:v>0.6?C.cyan:(v>0.3?'#1e3a5f':'#0d1626')},g));}
 var kern=E('rect',{x:24,y:30,width:px*3,height:px*3,fill:'none',stroke:C.gold,'stroke-width':2},g);
 var fmap=[];
 for(r=0;r<6;r++)for(c=0;c<6;c++){fmap.push(E('rect',{x:216+c*12,y:30+r*12,width:11,height:11,fill:'#0d1626',stroke:C.axis,'stroke-width':0.6},g));}
 return function(t){var cyc=t%7,total=36,idx=Math.min(35,Math.floor(cyc/7*36));
  var kr=Math.floor(idx/6),kc=idx%6;
  kern.setAttribute('x',24+kc*px);kern.setAttribute('y',30+kr*px);
  for(var i=0;i<=idx;i++){var fr=Math.floor(i/6),fc=i%6;
   fmap[i].setAttribute('fill',(fr+fc+idx)%3===0?C.emerald:(fr*fc%2? '#14532d':'#0d1626'));}
  for(i=idx+1;i<36;i++)fmap[i].setAttribute('fill','#0d1626');
 };
};
/* ---------- 25. ANN ---------- */
VIZ['ann']=function(g,W,H,R){
 grid(g,W,H);
 var layers=[4,5,3,2],xs=[60,150,240,315],nodes=[];
 layers.forEach(function(n,li){var ny=[];for(var i=0;i<n;i++){var y=40+i*(140/Math.max(1,n-1))+(n===1?70:0);
   if(n===1)y=110;
   ny.push(E('circle',{cx:xs[li],cy:y,r:9,fill:'#101a30',stroke:C.blue,'stroke-width':1.8},g));}nodes.push(ny);});
 var edges=[];
 for(var li=0;li<3;li++)nodes[li].forEach(function(a){nodes[li+1].forEach(function(b){
  edges.push({a:a,b:b,l:E('line',{x1:a.getAttribute('cx'),y1:a.getAttribute('cy'),x2:b.getAttribute('cx'),y2:b.getAttribute('cy'),stroke:'rgba(96,165,250,.22)','stroke-width':1},g)});});});
 var pulses=[];for(var p=0;p<7;p++){pulses.push({el:E('circle',{r:3.6,fill:C.gold},g),e:Math.floor(R()*edges.length),k:R()});}
 label(g,180,206,'forward pass — weighted sums through nonlinearities',C.blue,10,'middle');
 return function(t){
  pulses.forEach(function(pu){pu.k+=0.012;if(pu.k>1){pu.k=0;pu.e=Math.floor(R()*edges.length);}
   var e=edges[pu.e],x1=+e.a.getAttribute('cx'),y1=+e.a.getAttribute('cy'),x2=+e.b.getAttribute('cx'),y2=+e.b.getAttribute('cy');
   pu.el.setAttribute('cx',x1+(x2-x1)*pu.k);pu.el.setAttribute('cy',y1+(y2-y1)*pu.k);
   pu.el.setAttribute('opacity',Math.sin(pu.k*Math.PI));});
  nodes[3].forEach(function(n,i){n.setAttribute('stroke',C.emerald);});
 };
};
/* ---------- 26. Genetic Algorithms ---------- */
VIZ['genetic-algorithms']=function(g,W,H,R){
 grid(g,W,H);
 var bars=[],i;
 var fits=[];for(i=0;i<8;i++)fits.push(0.25+R()*0.75);
 function draw(y0){bars=[];for(i=0;i<8;i++){var h=fits[i]*90;
  bars.push(E('rect',{x:36+i*38,y:y0-h,width:24,height:h,fill:'#1e3a5f',stroke:C.axis,'stroke-width':1,rx:3},g));}}
 draw(190);
 var gen=label(g,320,24,'gen 1',C.gold,11,'end');
 label(g,24,208,'select → crossover → mutate',C.gold,10);
 var lastGen=1;
 function ranked(){return fits.map(function(f,i){return[f,i];}).sort(function(a,b){return b[0]-a[0];});}
 return function(t){var cyc=t%8,g2=1+Math.floor(cyc/2.6);
  if(g2!==lastGen){lastGen=g2;var rk=ranked(),p1=rk[0][0],p2=rk[1][0];
   for(var j=0;j<8;j++){fits[j]=Math.max(0.15,Math.min(1,((j%2?p1:p2))*0.9+R()*0.25));}
   bars.forEach(function(b){b.parentNode.removeChild(b);});draw(190);}
  gen.textContent='gen '+g2;
  var order=ranked();
  bars.forEach(function(b,i){var rank=order.findIndex(function(o){return o[1]===i;});
   b.setAttribute('fill',rank<2?C.emerald:'#1e3a5f');
   b.setAttribute('stroke',rank<2?C.emerald:C.axis);});
 };
};
/* ---------- 27. Markov Decision Process ---------- */
VIZ['markov-decision-process']=function(g,W,H,R){
 grid(g,W,H);
 var states=[[80,110,'S₀'],[180,60,'S₁'],[180,160,'S₂'],[290,110,'S₃']];
 states.forEach(function(s){E('circle',{cx:s[0],cy:s[1],r:24,fill:'#101a30',stroke:C.violet,'stroke-width':2},g);
  label(g,s[0],s[1]+4,s[2],C.text,11,'middle');});
 var trans=[
  {d:'M104,100 Q140,80 156,68',l:'a₀ p=.7 r=+1'},
  {d:'M104,122 Q140,142 156,152',l:'a₁ p=.3 r=−1'},
  {d:'M204,60 Q250,70 268,96',l:'p=.8 r=+5'},
  {d:'M204,160 Q250,150 268,124',l:'p=.6 r=0'},
  {d:'M180,84 L180,136',l:'p=.5'}];
 trans.forEach(function(tr){E('path',{d:tr.d,fill:'none',stroke:C.dim,'stroke-width':1.4},g);
  label(g,0,0,'',C.dim,8);});
 label(g,140,44,'a₀ p=.7 r=+1',C.dim,8,'middle');
 label(g,140,182,'a₁ p=.3 r=−1',C.dim,8,'middle');
 label(g,248,58,'p=.8 r=+5',C.dim,8,'middle');
 label(g,248,172,'p=.6 r=0',C.dim,8,'middle');
 var tok=E('circle',{r:8,fill:C.gold,stroke:'#7c5a10','stroke-width':2},g);
 var seq=[[80,110],[180,60],[290,110],[180,160],[80,110]];
 return function(t){var cyc=t%7.5,seg=cyc/1.5,idx=Math.floor(seg)%5,k=seg-Math.floor(seg);
  var a=seq[idx],b=seq[(idx+1)%5];
  tok.setAttribute('cx',a[0]+(b[0]-a[0])*k);tok.setAttribute('cy',a[1]+(b[1]-a[1])*k);};
};
/* ---------- 28. Isolation Forest ---------- */
VIZ['isolation-forest']=function(g,W,H,R){
 grid(g,W,H);
 var pts=[],i,x,y;
 for(i=0;i<22;i++){x=40+R()*200;y=40+R()*140;pts.push(E('circle',{cx:x,cy:y,r:3.2,fill:C.blue,opacity:.75},g));}
 var ax=300,ay=40;
 var ano=E('circle',{cx:ax,cy:ay,r:4.5,fill:C.rose,stroke:'#fff','stroke-width':1.2},g);
 label(g,ax,ay-12,'anomaly',C.rose,9,'middle');
 var splits=[
  {x1:270,y1:20,x2:270,y2:190},
  {x1:270,y1:20,x2:340,y2:20},
  {x1:120,y1:20,x2:120,y2:190},
  {x1:40,y1:100,x2:200,y2:100},
  {x1:160,y1:100,x2:160,y2:190}];
 var els=splits.map(function(s){var l=E('line',{x1:s.x1,y1:s.y1,x2:s.x2,y2:s.y2,stroke:C.emerald,'stroke-width':1.6,opacity:0},g);return l;});
 var score=label(g,24,206,'',C.rose,10);
 return function(t){var cyc=t%7;
  els.forEach(function(l,i){var k=Math.max(0,Math.min(1,(cyc-0.4-i*0.9)/0.5));l.setAttribute('opacity',k);});
  ano.setAttribute('r',4.5+1.5*Math.sin(t*4));
  score.textContent=cyc>2.2?'anomaly isolated in 2 splits — short path = outlier':'';
 };
};
/* ---------- 29. Autoencoders ---------- */
VIZ['autoencoders']=function(g,W,H,R){
 grid(g,W,H);
 var layers=[6,3,2,3,6],xs=[50,120,190,260,325],nodes=[];
 layers.forEach(function(n,li){var ny=[];for(var i=0;i<n;i++){var y=60+i*(100/Math.max(1,n-1));
   ny.push(E('circle',{cx:xs[li],cy:y,r:n===2?10:8,fill:'#101a30',stroke:li===2?C.gold:C.violet,'stroke-width':2},g));}nodes.push(ny);});
 for(var li=0;li<4;li++)nodes[li].forEach(function(a){nodes[li+1].forEach(function(b){
  E('line',{x1:a.getAttribute('cx'),y1:a.getAttribute('cy'),x2:b.getAttribute('cx'),y2:b.getAttribute('cy'),stroke:'rgba(167,139,250,.20)','stroke-width':1},g);});});
 label(g,50,180,'input',C.dim,9,'middle');label(g,190,180,'bottleneck',C.gold,9,'middle');label(g,325,180,'x̂ output',C.dim,9,'middle');
 var pulses=[];for(var p=0;p<6;p++)pulses.push(E('circle',{r:3.4,fill:C.pink},g));
 return function(t){var cyc=(t%4)/4;
  pulses.forEach(function(pu,i){var ph=(cyc+i/6)%1;
   var seg=ph*4,li=Math.min(3,Math.floor(seg)),k=seg-li;
   var a=nodes[li][i%nodes[li].length],b=nodes[li+1][i%nodes[li+1].length];
   var x1=+a.getAttribute('cx'),y1=+a.getAttribute('cy'),x2=+b.getAttribute('cx'),y2=+b.getAttribute('cy');
   pu.setAttribute('cx',x1+(x2-x1)*k);pu.setAttribute('cy',y1+(y2-y1)*k);pu.setAttribute('opacity',Math.sin(ph*Math.PI));});
 };
};

/* ================= framework ================= */
var mounts=[],io=null;
var reduceMotion=(window.matchMedia&&window.matchMedia('(prefers-reduced-motion: reduce)').matches);
function findMount(fig){for(var i=0;i<mounts.length;i++)if(mounts[i].fig===fig)return mounts[i];return null;}

/* ---- step pills: active pill derived from the animation time t ---- */
function activeStep(slug,t){
 var per=STEP_CYCLE[slug]||6,frac=(((t%per)+per)%per)/per,cuts=STEP_CUT[slug]||[],i=0;
 for(var k=0;k<cuts.length;k++)if(frac>=cuts[k])i=k+1;
 return i;
}
function paintSteps(m){
 if(!m.pills||!m.pills.length)return;
 var si=activeStep(m.slug,m.t);
 if(si===m.stepIdx)return;m.stepIdx=si;
 for(var i=0;i<m.pills.length;i++)m.pills[i].classList.toggle('on',i===si);
}

/* ---- component CSS (injected once; only touches the new aav-* classes) ---- */
var CSS_ONCE=false;
function injectCSS(){
 if(CSS_ONCE)return;CSS_ONCE=true;
 var st=document.createElement('style');st.setAttribute('data-aav-css','1');
 st.textContent=
 'figure.aav{position:relative;}'+
 '.aav-steps{display:flex;flex-wrap:wrap;gap:6px;margin:10px 0 6px;padding:0;}'+
 'figure.aav[data-orient="vertical"] .aav-steps{flex-direction:column;align-items:stretch;}'+
 '.aav-pill{display:inline-flex;align-items:center;gap:7px;padding:5px 12px 5px 6px;border-radius:999px;'+
 'font-family:ui-monospace,SFMono-Regular,Menlo,monospace;font-size:11px;line-height:1.4;color:#7d8aa0;'+
 'background:rgba(148,163,184,.07);border:1px solid rgba(148,163,184,.18);'+
 'transition:color .25s,border-color .25s,background-color .25s,box-shadow .25s;}'+
 '.aav-pill b{display:inline-flex;align-items:center;justify-content:center;min-width:17px;height:17px;border-radius:50%;'+
 'background:rgba(148,163,184,.16);color:#7d8aa0;font-size:10px;font-weight:700;}'+
 '.aav-pill.on{color:#d9f7fd;border-color:rgba(34,211,238,.6);background:rgba(34,211,238,.10);box-shadow:0 0 14px rgba(34,211,238,.22);}'+
 '.aav-pill.on b{background:#22d3ee;color:#052b33;}'+
 '.aav-tts{position:absolute;top:10px;right:10px;width:30px;height:30px;border-radius:50%;'+
 'border:1px solid rgba(148,163,184,.32);background:rgba(10,17,32,.82);color:#7d8aa0;cursor:pointer;'+
 'display:flex;align-items:center;justify-content:center;padding:0;z-index:2;'+
 'transition:color .2s,border-color .2s,box-shadow .2s;}'+
 '.aav-tts:hover{color:#22d3ee;border-color:rgba(34,211,238,.7);}'+
 '.aav-tts.playing{color:#22d3ee;border-color:#22d3ee;box-shadow:0 0 12px rgba(34,211,238,.45);}'+
 '.aav-tts:focus-visible{outline:2px solid #22d3ee;outline-offset:2px;}'+
 '.aav-tts svg{display:block;}';
 (document.head||document.documentElement).appendChild(st);
}

/* ---- Noah TTS narration toggle (lazy: no network/audio until the button is clicked) ---- */
var TTS_ICON='<svg viewBox="0 0 24 24" width="15" height="15" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><polygon points="11 5 6 9 2 9 2 15 6 15 11 19 11 5" fill="currentColor" stroke="none"/><path d="M15.5 8.5a5 5 0 0 1 0 7"/><path d="M18.5 5.5a9 9 0 0 1 0 13"/></svg>';
function ttsText(slug){
 var steps=(STEPS[slug]||[]).map(function(s,i){return (i+1)+'. '+s+'.';}).join(' ');
 return META[slug][0]+'. '+META[slug][1]+(steps?' Step by step: '+steps:'');
}
function wireTTS(btn,m){
 btn.innerHTML=TTS_ICON;
 btn.addEventListener('click',function(){
  if(m.audio){try{m.audio.pause();}catch(e){}m.audio=null;btn.classList.remove('playing');return;}
  btn.classList.add('playing');
  fetch('/api/noah/tts',{method:'POST',headers:{'Content-Type':'application/json'},
   body:JSON.stringify({text:ttsText(m.slug),voice:'narrator'})})
  .then(function(r){if(!r.ok)throw new Error('tts http '+r.status);
   var ct=(r.headers.get('content-type')||'').toLowerCase();
   if(ct.indexOf('audio')===0)return r.blob().then(function(b){return URL.createObjectURL(b);});
   return r.json().then(function(j){if(j&&j.url)return j.url;throw new Error('tts: no audio url');});})
  .then(function(url){
   var a=new Audio(url);m.audio=a;
   a.onended=function(){try{URL.revokeObjectURL(url);}catch(e){}m.audio=null;btn.classList.remove('playing');};
   a.onerror=function(){m.audio=null;btn.classList.remove('playing');};
   var pr=a.play();if(pr&&pr.catch)pr.catch(function(){m.audio=null;btn.classList.remove('playing');});})
  .catch(function(){btn.classList.remove('playing');btn.style.display='none';m.audio=null;});
 });
}

function mountFigure(fig){
 if(!fig||fig.getAttribute('data-aav-mounted'))return;
 var slug=fig.getAttribute('data-algo');
 if(!VIZ[slug]||!META[slug])return;
 injectCSS();
 fig.setAttribute('data-aav-mounted','1');
 var vert=fig.getAttribute('data-orient')==='vertical';
 var W=360,H=212;
 var svg=E('svg',{viewBox:vert?'0 0 220 390':'0 0 '+W+' '+H,'class':'aav-svg',role:'img','aria-label':META[slug][0]},null);
 if(vert){svg.style.width='100%';svg.style.height='auto';svg.style.display='block';}
 var target=svg;
 if(vert){var sc=220/W,ty=((390-H*sc)/2).toFixed(1);
  target=E('g',{transform:'translate(0 '+ty+') scale('+sc.toFixed(4)+')'},svg);}
 var stepsEl=document.createElement('div');stepsEl.className='aav-steps';
 var pills=(STEPS[slug]||[]).map(function(s,i){
  var p=document.createElement('span');p.className='aav-pill';
  var n=document.createElement('b');n.textContent=String(i+1);p.appendChild(n);
  var t=document.createElement('span');t.textContent=s;p.appendChild(t);
  stepsEl.appendChild(p);return p;});
 var cap=document.createElement('figcaption');cap.className='aav-cap';
 var st=document.createElement('strong');st.textContent=META[slug][0];
 var sp=document.createElement('span');sp.textContent=META[slug][1];
 cap.appendChild(st);cap.appendChild(sp);
 var btn=document.createElement('button');btn.type='button';btn.className='aav-tts';
 btn.setAttribute('aria-label','Narrate with Noah: '+META[slug][0]);btn.title='Narrate with Noah';
 fig.appendChild(svg);fig.appendChild(stepsEl);fig.appendChild(cap);fig.appendChild(btn);
 var R=mulberry(hash(slug));
 var update;
 try{update=VIZ[slug](target,W,H,R);}catch(e){return;}
 var m={fig:fig,slug:slug,update:update,visible:false,t:R()*8,pills:pills,stepIdx:-1,audio:null};
 wireTTS(btn,m);
 mounts.push(m);
 if(reduceMotion){m.t=2.8;try{update(2.8,0);}catch(e){}}
 else if(io){io.observe(fig);}else{m.visible=true;}
 paintSteps(m);
}
function scan(root){
 (root||document).querySelectorAll('figure.aav[data-algo]').forEach(mountFigure);
}
function boot(){
 if('IntersectionObserver' in window){
  io=new IntersectionObserver(function(es){es.forEach(function(e){var m=findMount(e.target);if(m)m.visible=e.isIntersecting;});},{threshold:0.12,rootMargin:'80px'});
 }
 scan(document);
 if(!reduceMotion){
  var last=0;
  (function tick(now){var t=now/1000,dt=Math.min(0.06,last?t-last:0.016);last=t;
   for(var i=0;i<mounts.length;i++){var m=mounts[i];if(m.visible&&m.update){m.t+=dt;try{m.update(m.t,dt);}catch(e){}paintSteps(m);}}
   requestAnimationFrame(tick);})(0);
 }
 if('MutationObserver' in window){
  var mo=new MutationObserver(function(muts){muts.forEach(function(mu){
   mu.addedNodes.forEach(function(n){if(n.nodeType!==1)return;
    if(n.matches&&n.matches('figure.aav[data-algo]'))mountFigure(n);
    else if(n.querySelectorAll)n.querySelectorAll('figure.aav[data-algo]').forEach(mountFigure);});});});
  mo.observe(document.documentElement,{childList:true,subtree:true});
 }
}
window.AIAlgoViz={refresh:function(){scan(document);}};
if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',boot);
else boot();
})();
