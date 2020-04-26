import cv2
import numpy as np
import matplotlib.pyplot as plt
import math as m
import queue
import random
try:
    import xml.etree.CElementTree as ET
except:
    import xml.etree.ElementTree as ET
w=1000
h=700

def putText(text,pos):
    global img
    cv2.putText(img, text, pos, cv2.FONT_HERSHEY_PLAIN, 2.0, (0, 0, 255), 2)

def DrawLine(pos1,pos2):
    global img
    cv2.line(img, pos1, pos2, (0,0,0), 2, 4)

class Tree:
    def __init__(self,value):
        self.value=value
        self.children=[]
        self.pos=(0,0)
    def appendSon(self,value):
        self.children.append(Tree(value))
    def getChildren(self,index):
        return self.children[index]
    def drawTree(self):
        tree=self
        global  w
        q=queue.Queue()
        q.put(tree)
        pos=(w//2,30)
        tree.pos=pos
        while(q.empty()==0):
            tree=q.get()
            x,y=tree.pos
            y+=15
            pos=(x,y)
            putText(tree.value,pos)
            for i in range(len(tree.children)):
                n = len(tree.children)
                child=tree.getChildren(i)
                q.put(child)
                angle=180-180/(n+1)*(i+1)
                radian=angle*m.pi/180
                k=m.tan(radian)
                new_y=y+80
                new_x=int(x-(y-new_y)/k)
                new_pos=(new_x,new_y)
                DrawLine(pos,new_pos)
                new_y+=25
                new_x-=0
                new_pos = (new_x, new_y)
                child.pos=new_pos


def traverseXml(element):
    #print (len(element))
    if len(element)>0:
        for child in element:
            print (child.tag, "----", child.attrib)
            traverseXml(child)

def readXml(filename):
    xml_tree = ET.parse(filename)
    root=xml_tree.getroot()
    q=queue.Queue()
    treeQ=queue.Queue()
    q.put(root)
    st=Tree('E')
    treeQ.put(st)
    while(q.empty()==0):
        node=q.get()
        t=treeQ.get()
        if(node.tag=='op'):
            t.value=node.text
        else:
            t.value=node.tag
        i=0
        for child in node:
            q.put(child)
            t.appendSon(child.tag)
            treeQ.put(t.getChildren(i))
            i+=1
            # print("遍历root的下一层", child.tag, )
    return st



if __name__ == '__main__':
    st=readXml('tree.xml')
    print('读取xml文件完成')
    img=np.full((h,w),255)
    img=img.astype('uint8')

    st.drawTree()
    print('画语法树完成')

    plt.figure(figsize=(10,8))
    plt.imshow(img,cmap='gray')

    plt.show()


