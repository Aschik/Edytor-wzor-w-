import sys,os
import math
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtGui import QPixmap, QIcon, QFont
import tempfile
import subprocess
import json

#---------------------Zmienne Globalne---------------------


BUTTON_ICON_SIZE      = 16        # function button size
THUMBNAIL_SIZE        = 36        # thumbnail button size in preset
MATRIX_THUMBNAIL_SIZE = 48        # thumbnail size for matrix icons in preset
HIST_THUMBNAIL_SIZE   = 60        # thumbnail button size in history/favorites
BUTTON_FONT_SIZE      = 11        # font size for buttons
TEXT_EDIT_FONT        = 13        # font size for formula edit box
ICON_NCOL             = 5         # number of columns in preset
MATRIX_ICON_NCOL      = 4         # number of columns in matrix preset
TAB_NCOL              = 2         # number of columns for tab icons
DEFAULT_RESO          = 150
CURRENT_DIR           = os.path.dirname(os.path.abspath(__file__))
ICON_META_FILE        = os.path.join(CURRENT_DIR, 'icon_paths.txt')   # preset file
TEX2IM_CMD            = os.path.join(CURRENT_DIR,'tex2im/tex2im')  # tex2im exe path
DEMO_IMG              = os.path.join(CURRENT_DIR,'tab_icons/demo.png') # demo img


DEMO_FORMULA=\
r'''\int_z^{\infty} \frac{dI}{I} = - \int_z^{\infty} \rho k_{\lambda}sec \theta dz
'''

def getHSpacer():
    h_spacer = QtWidgets.QSpacerItem(0,0,QtWidgets.QSizePolicy.Expanding,
            QtWidgets.QSizePolicy.Minimum)
    return h_spacer

def getVSpacer():
    v_spacer = QtWidgets.QSpacerItem(0,0,QtWidgets.QSizePolicy.Minimum,
            QtWidgets.QSizePolicy.Expanding)
    return v_spacer

def getVLine(parent):
    v_line = QtWidgets.QFrame(parent)
    v_line.setFrameShape(QtWidgets.QFrame.VLine)
    v_line.setFrameShadow(QtWidgets.QFrame.Sunken)
    return v_line

def getHLine(parent):
    h_line = QtWidgets.QFrame(parent)
    h_line.setFrameShape(QtWidgets.QFrame.HLine)
    h_line.setFrameShadow(QtWidgets.QFrame.Sunken)
    return h_line


def getMinSizePolicy():
    sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum,
            QtWidgets.QSizePolicy.Minimum)
    return sizePolicy

def getXMinYExpandSizePolicy():
    sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum,
            QtWidgets.QSizePolicy.Expanding)
    return sizePolicy

def getXExpandYMinSizePolicy():
    sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding,
            QtWidgets.QSizePolicy.Minimum)
    return sizePolicy

def getXExpandYExpandSizePolicy():
    sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding,
            QtWidgets.QSizePolicy.Expanding)
    return sizePolicy



#-----Renderowanie poszczególnej formuły i zapis do img-----
def renderFormula(text,reso,outfile=None):
    if len(text)==0:
        return 2, None

    reso_str='%dx%d' %(reso,reso)

    #------------Get a random tmp file name------------
    tmp_tex_fd,tmp_tex_file=tempfile.mkstemp(suffix='.tex',prefix='tmp_latex_',
            dir='/tmp')
    if outfile is None:
        tmp_img_fd,tmp_img_file=tempfile.mkstemp(suffix='.png',prefix='tmp_latex_',
                dir='/tmp')
    else:
        tmp_img_file=outfile

    #------------Wywołanie tex2im aby renderować do img------------
    try:
        tfile=os.fdopen(tmp_tex_fd,'w')
        tfile.write(text)
        tfile.close()
        cmd='%s -r %s -o %s %s' %(TEX2IM_CMD,reso_str,tmp_img_file,tmp_tex_file)
        proc=subprocess.Popen(cmd,stdout=subprocess.PIPE,stderr=subprocess.PIPE,shell=True)
        rec=proc.wait()
    except:
        rec=1
    finally:
        os.remove(tmp_tex_file)

    return rec,tmp_img_file



class MainFrame(QtWidgets.QWidget):

    def __init__(self,thumbnail_meta_list):
        super(MainFrame,self).__init__()

        self.thumbnail_meta_list=thumbnail_meta_list
        self.thumbnail_btn_dict={}    # buttons for preset icons


        #-------------------Przyciski------------------
        self.tab_btn_dict={}
        self.initUI()


    def getThumbnailFrame(self,icon_size,thumbnail_list,nrow=None,ncol=None):
        '''Get thumbnail frame for preset icons
        '''

        frame=QtWidgets.QWidget()
        grid=QtWidgets.QGridLayout()
        grid.setSpacing(0)

        #------------------Wielkość grida------------------
        nlist=len(thumbnail_list)
        if nrow is None and ncol is not None:
            nrow=max(1,int(math.ceil(nlist/float(ncol))))
        elif nrow is not None and ncol is None:
            ncol=max(1,int(math.ceil(nlist/float(nrow))))
        else:
            raise Exception("Error")

        #---------------Add buttons to grid---------------
        positions=[(ii,jj) for ii in range(nrow) for jj in range(ncol)]

        for posii,thumbnailii in zip(positions,thumbnail_list):
            icon_textii,icon_img_pathii=thumbnailii
            icon_img_pathii=os.path.join(CURRENT_DIR, icon_img_pathii)
            buttonii=QtWidgets.QToolButton(self)
            buttonii.setIcon(QIcon(icon_img_pathii))
            buttonii.setIconSize(QtCore.QSize(icon_size,icon_size))
            buttonii.setStyleSheet('background-color:rgb(255,255,255)')
            grid.addWidget(buttonii,*posii)
            self.thumbnail_btn_dict[buttonii]=thumbnailii
            buttonii.clicked.connect(self.thumbnail_btn_click)

            grid.setRowStretch(posii[0],0)
            grid.setColumnStretch(posii[1],0)

        grid.addItem(getVSpacer(),nrow,0)
        grid.addItem(getHSpacer(),0,ncol)
        frame.setLayout(grid)

        return frame

    def getStackedWidget(self):
        '''Utworzenie zestawu widżetów do przechowywania różnych stron z miniaturami
        '''

        v_layout=QtWidgets.QVBoxLayout()
        grid=QtWidgets.QGridLayout()
        self.stack=QtWidgets.QStackedWidget(self)

        for ii,itemii in enumerate(self.thumbnail_meta_list):

            stack_nameii,icon_listii=itemii

            #--------Ustawienie miniatur--------
            scrollii=QtWidgets.QScrollArea(self)
            scrollii.setWidgetResizable(True)

            if stack_nameii=='Matrix':
                icon_size=MATRIX_THUMBNAIL_SIZE
                icon_ncol=MATRIX_ICON_NCOL
            else:
                icon_size=THUMBNAIL_SIZE
                icon_ncol=ICON_NCOL

            grid_frameii=self.getThumbnailFrame(icon_size,icon_listii,
                    ncol=icon_ncol)
            scrollii.setWidget(grid_frameii)

            self.stack.addWidget(scrollii)

            #--------------Utworzenie przycisku stacku--------------
            buttonii=QtWidgets.QPushButton(stack_nameii,self)
            buttonii.setSizePolicy(getMinSizePolicy())

            #---------------Ustawienie wielkosci fontu przycisku---------------
            font=buttonii.font()
            font.setPointSize(BUTTON_FONT_SIZE)
            buttonii.setFont(font)

            #-----Przechowuje button index i łączenie----
            self.tab_btn_dict[buttonii]=ii
            buttonii.clicked.connect(self.tab_btn_click)

            grid.addWidget(buttonii,ii//TAB_NCOL,ii%TAB_NCOL)

        grid.addItem(getHSpacer(),0,TAB_NCOL)
        v_layout.addLayout(grid)
        v_layout.addWidget(self.stack)
        self.stack.setSizePolicy(getMinSizePolicy())


        return v_layout



    #---------Kliknięcie przycisku presetu ramki---------
    def thumbnail_btn_click(self):
        icon_text,icon_img_path=self.thumbnail_btn_dict[self.sender()]
        self.text_box.setFontPointSize(TEXT_EDIT_FONT)
        self.text_box.insertPlainText(icon_text)

    def tab_btn_click(self):
        idx=self.tab_btn_dict[self.sender()]
        self.stack.setCurrentIndex(idx)



    def getTextFrame(self):
        '''Utwórz ramkę dla pola edycji tekstu i przycisków edycji

        '''

        v_layout=QtWidgets.QVBoxLayout()
        h_layout=QtWidgets.QHBoxLayout()

        self.clip_board=QtWidgets.QApplication.clipboard()

        #------------Add buttons for text frame------------
        self.undo_button=QtWidgets.QToolButton()
        self.redo_button=QtWidgets.QToolButton()
        self.cut_button=QtWidgets.QToolButton()
        self.txt_copy_button=QtWidgets.QToolButton()
        self.paste_button=QtWidgets.QToolButton()

        buttons=[self.undo_button, self.redo_button, self.cut_button,
                self.txt_copy_button, self.paste_button]

        icon_names=['Cofnij','Ponów','Wytnij','Kopiuj','Wklej']

        for ii,nameii in enumerate(icon_names):
            buttonii=buttons[ii]
            buttonii.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
            buttonii.setText(nameii)

        for bii in buttons:
            h_layout.addWidget(bii)

        h_layout.addItem(getHSpacer())
        v_layout.addLayout(h_layout)

        #------------------Dodanie text edit------------------
        self.text_box=QtWidgets.QTextEdit()
        font=QFont()
        font.setPointSize(TEXT_EDIT_FONT)
        self.text_box.setFont(font)
        self.text_box.setText(DEMO_FORMULA)
        v_layout.addWidget(self.text_box)

        #-----------------Connect przyciskow-----------------
        self.txt_copy_button.clicked.connect(self.text_box.copy)
        self.paste_button.clicked.connect(self.text_box.paste)
        self.cut_button.clicked.connect(self.text_box.cut)
        self.undo_button.clicked.connect(self.text_box.undo)
        self.redo_button.clicked.connect(self.text_box.redo)

        frame=QtWidgets.QFrame(self)
        frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        frame.setLayout(v_layout)

        return frame


    def getImageFrame(self):

        v_layout=QtWidgets.QVBoxLayout()
        h_layout=QtWidgets.QHBoxLayout()

        #-------------Dodanie przyciskow-------------

        #----------------Dodanie przycisku Zapisz----------------
        self.img_save_button=QtWidgets.QToolButton()
        self.img_save_button.setText('Zapisz')
        self.img_save_button.clicked.connect(self.img_save_btn_click)

        h_layout.addWidget(self.img_save_button)


        self.img_slider=QtWidgets.QSlider(QtCore.Qt.Horizontal,self)
        self.img_slider.setMinimum(50)
        self.img_slider.setMaximum(1000)
        self.img_slider.setTickInterval(50)
        self.img_slider.setTickPosition(QtWidgets.QSlider.TicksBelow)
        self.img_slider.setSingleStep(50)
        self.img_slider.setValue(DEFAULT_RESO)
        self.img_slider.valueChanged[int].connect(self.slider_change_value)

        h_layout.addStretch()


        self.slider_text=QtWidgets.QLineEdit(self)
        self.slider_text.setText(str(DEFAULT_RESO))

        self.slider_text.setFixedWidth(80)
        self.slider_text.setSizePolicy(getMinSizePolicy())
        self.slider_text.returnPressed.connect(self.dpi_box_change_value)

        scroll=QtWidgets.QScrollArea(self)
        scroll.setWidgetResizable(True)

        self.img_label=QtWidgets.QLabel()
        self.img_pixmap=QPixmap(DEMO_IMG)
        self.img_file_path=DEMO_IMG
        self.img_label.setPixmap(self.img_pixmap)

        scroll.setWidget(self.img_label)
        self.img_label.setAlignment(QtCore.Qt.AlignCenter)

        h_layout.addWidget(self.img_slider)
        h_layout.addWidget(self.slider_text)
        h_layout.setAlignment(QtCore.Qt.AlignTop)
        v_layout.addLayout(h_layout)
        v_layout.addWidget(scroll)



        return v_layout



    #------Przycisk i slider funkcje----
    def slider_change_value(self):
        v=self.img_slider.value()
        v2=v//50*50
        self.img_slider.setValue(v2)
        self.slider_text.setText(str(v2))

    def dpi_box_change_value(self):
        v=int(self.slider_text.text())
        self.img_slider.setValue(v)


    def img_save_btn_click(self):
        if self.img_label.pixmap() is not None:
            filename=QtWidgets.QFileDialog.getSaveFileName(self, 'Zapisz obraz',
                    os.getenv('HOME'),'*.png')
            if len(filename[0])>0:
                self.img_pixmap.save(filename[0])


    def render_btn_click(self):
        '''Funkcja render
        '''

        text=self.text_box.toPlainText()
        reso=self.img_slider.value()
        rec,tmp_img_file=renderFormula(text,reso,None)

        if rec==0:
            self.img_pixmap=QPixmap(tmp_img_file)
            self.img_label.setPixmap(self.img_pixmap)
            self.img_file_path=tmp_img_file

            return 0

        elif rec==2 and tmp_img_file is None:
            #--------------------Empty text--------------------
            self.img_copy_button.setEnabled(False)
            self.img_save_button.setEnabled(False)
            self.img_addfav_button.setEnabled(False)
            return 1
        else:
            self.img_label.setPixmap(self.img_pixmap)
            self.img_copy_button.setEnabled(False)
            self.img_save_button.setEnabled(False)
            self.img_addfav_button.setEnabled(False)
            return 1




    def initUI(self):

        self.setWindowTitle('LaTeX formula editor')

        #---------------Dodanie pionowego layoutu---------------
        v_layout0=QtWidgets.QVBoxLayout(self)

        #-------------------Dodanie pierwszego wiersza-------------------
        h_layout0=QtWidgets.QHBoxLayout()
        v_layout0.addLayout(h_layout0)
        h_layout0.addLayout(self.getStackedWidget())
        h_layout0.setStretch(0,0)

        v_layout1=QtWidgets.QVBoxLayout()
        h_layout0.addLayout(v_layout1)
        h_layout0.setStretch(1,1)

        #------------------Edit------------------
        v_layout1.addWidget(self.getTextFrame())

        h_layout1=QtWidgets.QHBoxLayout()
        h_layout1.addWidget(getHLine(self),alignment=QtCore.Qt.AlignVCenter)

        #----------------Dodanie przycisku render----------------
        self.render_button=QtWidgets.QToolButton(self)
        self.render_button.setIconSize(QtCore.QSize(BUTTON_ICON_SIZE,BUTTON_ICON_SIZE))
        self.render_button.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)
        self.render_button.setText('Renderuj')
        self.render_button.clicked.connect(self.render_btn_click)

        h_layout1.addWidget(self.render_button)
        h_layout1.addWidget(getHLine(self),alignment=QtCore.Qt.AlignVCenter)

        v_layout1.addLayout(h_layout1)

        v_layout1.addLayout(self.getImageFrame())

        self.show()


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self,thumbnail_meta_list):
        super(MainWindow,self).__init__()

        self.main_frame=MainFrame(thumbnail_meta_list)
        self.setCentralWidget(self.main_frame)
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Formuła1 Inżynieria Oprogramowania')
        self.setGeometry(100,100,1200,900)
        self.show()


if __name__=='__main__':

    with open(ICON_META_FILE,'r') as fin:
        thumbnail_meta_list=json.load(fin)

    app=QtWidgets.QApplication(sys.argv)
    mainwindow=MainWindow(thumbnail_meta_list)
    sys.exit(app.exec_())




