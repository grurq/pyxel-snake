import sys
import pyxel

class body:
	WIDTH=8
	HEIGHT=8
	HCOLOR=10
	BCOLOR=11
	length=5
	vector=0
	bodyX=[]
	bodyY=[]
	"""
	vector(方向)は
	1が上向き 3x
	2が右向き 4x
	3が下向き 1x
	4が左向き 2x
	の順である。xの方向へは移動できない
	"""
	def __init__(self):
		x=pyxel.rndi(4,16)
		y=pyxel.rndi(4,8)
		self.vector=pyxel.rndi(1,4)
		if self.vector==1: # 上向き
			for i in range(self.length):
				self.bodyX.append(x)
				self.bodyY.append(y+i)
		elif self.vector==2: # 右向き
			for i in range(self.length) : 
				self.bodyX.append(x-i)
				self.bodyY.append(y)
		elif self.vector==3: # 下向き
			for i in range(self.length) : 
				self.bodyX.append(x)
				self.bodyY.append(y-i)
		elif self.vector==4: # 左向き
			for i in range(self.length) : 
				self.bodyX.append(x+i)
				self.bodyY.append(y)			
				
	def put(self,num):
		color=0
		if num ==0:
			color=self.HCOLOR
		elif num <self.length:
			color=self.BCOLOR
		pyxel.rect(self.bodyX[num]*self.WIDTH,self.bodyY[num]*self.HEIGHT,self.WIDTH,self.HEIGHT,color)

	def erase(self):
		self.bodyX.clear()
		self.bodyY.clear()
		
	def extend(self):
		NX=self.bodyX[0]
		NY=self.bodyY[0]
		clashed=False
		if self.vector==1: # 上向き
			self.bodyX.insert(0,NX)
			self.bodyY.insert(0,NY-1)
		elif self.vector==2: # 右向き 
			self.bodyX.insert(0,NX+1)
			self.bodyY.insert(0,NY)
		elif self.vector==3: # 下向き 
			self.bodyX.insert(0,NX)
			self.bodyY.insert(0,NY+1)
		elif self.vector==4: # 左向き
			self.bodyX.insert(0,NX-1)
			self.bodyY.insert(0,NY)	
		if self.bodyX[0]<0:
			self.bodyX[0]=19
		if self.bodyX[0]>19:
			self.bodyX[0]=0
		if self.bodyY[0]<0:
			self.bodyY[0]=13
		if self.bodyY[0]>13:
			self.bodyY[0]=0
		for i in range(len(self.bodyX)):
			if i>1:
				if self.bodyX[0]==self.bodyX[i] and self.bodyY[0]==self.bodyY[i]:
					clashed=True
		return clashed
			
	def shrink(self):
		blength=len(self.bodyX)
		if blength>self.length:
			self.put(blength-1)
			del self.bodyX[-1]
			del self.bodyY[-1]

class feed:
	X=0
	Y=0
	WIDTH=8
	HEIGHT=8
	FCOLOR=8
	RADUIS=4
	def __init__(self):
		self.X=0
		self.Y=0
	
	def put(self):
		pyxel.rect(self.X*self.WIDTH,self.Y*self.HEIGHT,self.WIDTH,self.HEIGHT,0)
		pyxel.circ(self.X*self.WIDTH+self.RADUIS,self.Y*self.HEIGHT+self.RADUIS,self.RADUIS-1,self.FCOLOR)
	
class App:
	fps=0
	FPS_MAX=30
	snake: body
	fruit: feed
	scene=0 # 0:開始前 1:プレイ中 2:衝突 3:ポーズ 4:終了　を示す制御変数
	READY=0
	PLAY=1
	MISS=2
	PAUSE=3
	END=4
	lengthmax=5
	invector=False

	def __init__(self):
		pyxel.init(160, 120,title="SNAKE GAME by grurqApps 2026")
		pyxel.load("snake.pyxres")
		pyxel.cls(0)
		pyxel.text(0,113,"SNAKE",7)
		# 以下の行は初期設定として後でメソッド化
		self.ready()
		pyxel.run(self.update, self.draw)

	def feedput(self):
		put=False
		putx=0
		puty=0
		while put==False:
			putx=pyxel.rndi(0,19)
			puty=pyxel.rndi(0,13)
			put=True
			for i in range(len(self.snake.bodyX)):
				if putx==self.snake.bodyX[i] and puty==self.snake.bodyY[i]:
					put=False
		self.fruit.X=putx
		self.fruit.Y=puty
		self.fruit.put()				
			
	def ready(self):
		self.fps=0
		self.invector=False
		self.scene=self.READY
		pyxel.text(100,113,"READY",7)
		self.snake=body()
		self.fruit=feed()
		self.textbody()
		self.textlengthmax()
		
		for i in range(self.snake.length):
			self.snake.put(i)
		self.feedput()
		
	def textbody(self):
		body = f"BODY:{self.snake.length:03}"
		pyxel.rect(30,113,32,6,0)
		pyxel.text(30,113,body,7)

	def textlengthmax(self):
		lengthmax = f"MAX:{self.lengthmax:03}"
		pyxel.rect(64,113,28,6,0)
		pyxel.text(64,113,lengthmax,7)

	def cls(self):
		pyxel.rect(0,0,160,112,0)
		pyxel.rect(100,113,20,6,0)	
		
	def update(self):
		if self.scene==self.PLAY and ( pyxel.btnp(pyxel.KEY_I) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_DPAD_UP)) and self.snake.vector != 3: #上
				if self.invector==False:
					self.snake.vector=1
					self.invector=True
		if self.scene==self.PLAY and ( pyxel.btnp(pyxel.KEY_L) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_DPAD_RIGHT)) and self.snake.vector != 4: #右
				if self.invector==False:
					self.snake.vector=2
					self.invector=True
		if self.scene==self.PLAY and ( pyxel.btnp(pyxel.KEY_K) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_DPAD_DOWN)) and self.snake.vector != 1: #下
				if self.invector==False:
					self.snake.vector=3
					self.invector=True
		if self.scene==self.PLAY and ( pyxel.btnp(pyxel.KEY_J) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_DPAD_LEFT)) and self.snake.vector != 2: #左
				if self.invector==False:
					self.snake.vector=4
					self.invector=True
		if self.scene==self.MISS:
			if pyxel.btnp(pyxel.KEY_SPACE) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_START):
				self.snake.erase()
				self.cls()
				self.ready()	
		elif self.scene==self.READY:
			if pyxel.btnp(pyxel.KEY_SPACE) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_START):
				self.scene=self.PLAY
				pyxel.rect(100,113,20,6,0)
		elif self.scene==self.PAUSE:
			if pyxel.btnp(pyxel.KEY_SPACE) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_START):
				self.scene=self.PLAY
				pyxel.play(1,1)
				pyxel.rect(100,113,20,6,0)
		elif self.scene==self.PLAY and ( pyxel.btnp(pyxel.KEY_SPACE) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_START)):
			pyxel.text(100,113,"PAUSE",7)
			self.scene=self.PAUSE
			pyxel.play(1,1)
			
		self.fps = self.fps + 1
		if self.fps == self.FPS_MAX:
			self.fps = 0 
	
	def draw(self):
		clashed=False
		if self.fps % 5 == 0:
			if self.scene==self.PLAY:
				self.invector=False
				clashed=self.snake.extend()
				# if self.fps % 10 ==0:
				pyxel.play(0,0)
				if clashed==True:
					pyxel.text(100,113,"MISS!",7)
					pyxel.play(1,2)
					self.scene=self.MISS
					MISS=True
					if self.snake.length>self.lengthmax:
						self.lengthmax=self.snake.length
					return
				if self.fruit.X==self.snake.bodyX[0] and self.fruit.Y==self.snake.bodyY[0]:
					self.feedput()
					self.snake.length=self.snake.length+1
					self.textbody()
					pyxel.play(1,1)
				self.snake.shrink()
				self.snake.put(0)
				self.snake.put(1)
			elif self.scene==self.END:
				sys.exit()
				
App()
