#Autogenerated by ReportLab guiedit do not edit
from reportlab.graphics.shapes import _DrawingEditorMixin, Drawing, Group, Line, String
from reportlab.lib.colors import Color, CMYKColor, PCMYKColor

class ExplodedDrawing_Drawing(_DrawingEditorMixin,Drawing):
	def __init__(self,width=200,height=100,*args,**kw):
		Drawing.__init__(self,width,height,*args,**kw)
		self.transform = (1,0,0,1,0,0)
		self.add(Line(20,88,30,88,strokeColor=Color(1,0,0,1),strokeWidth=1,strokeLineCap=0,strokeLineJoin=0,strokeMiterLimit=0,strokeDashArray=[2,1],strokeOpacity=None))
		self.add(String(40,85.585,'red',textAnchor='start',fontName='Times-Roman',fontSize=10,fillColor=Color(0,0,0,1)))
		self.add(Line(20,68,30,68,strokeColor=Color(0,.501961,0,1),strokeWidth=1,strokeLineCap=0,strokeLineJoin=0,strokeMiterLimit=0,strokeDashArray=[2,5],strokeOpacity=None))
		self.add(String(40,65.585,'green',textAnchor='start',fontName='Times-Roman',fontSize=10,fillColor=Color(0,0,0,1)))
		self.add(Line(20,48,30,48,strokeColor=Color(0,0,1,1),strokeWidth=1,strokeLineCap=0,strokeLineJoin=0,strokeMiterLimit=0,strokeDashArray=[2,2,5,5],strokeOpacity=None))
		self.add(String(40,45.585,'blue',textAnchor='start',fontName='Times-Roman',fontSize=10,fillColor=Color(0,0,0,1)))
		self.add(Line(20,28,30,28,strokeColor=Color(1,1,0,1),strokeWidth=1,strokeLineCap=0,strokeLineJoin=0,strokeMiterLimit=0,strokeDashArray=[1,2,3,4],strokeOpacity=None))
		self.add(String(40,25.585,'yellow',textAnchor='start',fontName='Times-Roman',fontSize=10,fillColor=Color(0,0,0,1)))
		self.add(Line(80,88,90,88,strokeColor=Color(1,.752941,.796078,1),strokeWidth=1,strokeLineCap=0,strokeLineJoin=0,strokeMiterLimit=0,strokeDashArray=[4,2,3,4],strokeOpacity=None))
		self.add(String(100,85.585,'pink',textAnchor='start',fontName='Times-Roman',fontSize=10,fillColor=Color(0,0,0,1)))
		self.add(Line(80,68,90,68,strokeColor=Color(0,0,0,1),strokeWidth=1,strokeLineCap=0,strokeLineJoin=0,strokeMiterLimit=0,strokeDashArray=[1,2,3,4,5,6],strokeOpacity=None))
		self.add(String(100,65.585,'black',textAnchor='start',fontName='Times-Roman',fontSize=10,fillColor=Color(0,0,0,1)))
		self.add(Line(80,48,90,48,strokeColor=Color(1,1,1,1),strokeWidth=1,strokeLineCap=0,strokeLineJoin=0,strokeMiterLimit=0,strokeDashArray=[1],strokeOpacity=None))
		self.add(String(100,45.585,'white',textAnchor='start',fontName='Times-Roman',fontSize=10,fillColor=Color(0,0,0,1)))


if __name__=="__main__": #NORUNTESTS
	ExplodedDrawing_Drawing().save(formats=['pdf'],outDir='.',fnRoot=None)
