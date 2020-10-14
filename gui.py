from tkinter import Tk, Button, Frame, Label, mainloop, Checkbutton, StringVar, BooleanVar, Entry,Radiobutton
from collections import namedtuple,defaultdict
from Project import Validation
from Databases import Database
from os import chdir
from Packages.Utils import InputUtils

# Pesticides in Honey
# Κατερίνα Κορωνία, Αλέξανδρος Ρόδης, Αποστόλης Καραγιαννίδης,Γιώργος Κουλής, Νικόλαος Θωμαΐδης
# H:\Pesticides Honey\Results\GC\Method Validation\Excel Exports
# C:\Users\User\Desktop\HoneyPesticides



class IntroScreen:

    def __init__(self, root):
        intro_font = gui_font(letterfont, 10)
        self.root = root
        # Implement geometry logic. Weird namespace errors
        self.root.geometry("960x750")
        self.root.mainframe = Frame(self.root, bg='coral').place(
            relx=0, rely=0, relwidth=1, relheight=1)
        self.root.btn_new = Button(
            self.root.mainframe, text="New Project", font=intro_font, command=lambda: ProjectTypeScreen(self.root))
        self.root.btn_new.place(relx=0.2, rely=0.5)
        self.root.btn_open = Button(
            self.root.mainframe, font=intro_font, text="Open Project", state='disabled')
        self.root.btn_open.place(relx=0.4, rely=0.5)
        self.root.btn_ext = Button(
            self.root.mainframe, text="Exit", font=intro_font, command=self.root.quit, padx=10, pady=2.3)
        self.root.btn_ext.place(relx=0.6, rely=0.5)


class ProjectTypeScreen(InputUtils):

    def moveahead(self):
        datapath,filepath = self.datapathentry.get(),self.projectpathentry.get()
        settings={}
        try:
            chdir(datapath)
        except FileNotFoundError:
             print("Data Path not found")
        settings['project_parameters']={'name':self.projectnameentry.get(),'team':super().convert_input(self.projectteamentry.get(),typ='string'),'datapath':datapath,'filepath':filepath}
        MethodValidationScreen(self.root,settings)

    def add_features(self):
        self.projectnamelabel = Label(self.root.mainframe,text="Project Name: ",font=(letterfont,12),bg='green')
        self.projectnamelabel.place(relx=.1,rely=.15)
        self.projectnameentry=Entry(self.root.mainframe)
        self.projectnameentry.place(relx=.2,rely=.15)
        self.projectteamlabel=Label(self.root.mainframe,text="Project Team Members",font=(letterfont,12),bg='green',wraplength=100)
        self.projectteamlabel.place(rely=.2,relx=.1)
        self.projectteamentry=Entry(self.root.mainframe)
        self.projectteamentry.place(relx=.2,rely=.2)
        self.datapathlabel=Label(self.root.mainframe,text="Path to Data: ",font=(letterfont,12),bg='green')
        self.datapathlabel.place(relx=.6,rely=.15)
        self.datapathentry=Entry(self.root.mainframe)
        self.datapathentry.place(relx=.7,rely=.15)
        self.projectpathlabel=Label(self.root.mainframe,text="Project File Path: ",font=(letterfont,12),bg='green',wraplength=100)
        self.projectpathlabel.place(relx=.6,rely=.2)
        self.projectpathentry=Entry(self.root.mainframe)
        self.projectpathentry.place(relx=.7,rely=.2)
        self.btn_ok=Button(self.root.mainframe,text="OK",font =(letterfont,12),command=self.moveahead)
        # self.btn_ok.pack()
        self.btn_cnl=Button(self.root.mainframe,text="Exit",font =(letterfont,12),command=self.root.quit)
        # self.btn_cnl.pack()



    def __init__(self, root):
        intro_font = gui_font(letterfont, 10)
        self.root = root
        self.root.geometry("960x750")
        self.root.mainframe = Frame(self.root, bg='blue').place(
            relx=0, rely=0, relwidth=1, relheight=1)
        self.btn_library = Button(
            self.root.mainframe, font=intro_font, text="Build Analyte Library", state='disabled')
        self.btn_library.place(relx=0.15, rely=0.5)
        self.btn_method = Button(
            self.root.mainframe, font=intro_font, text="Create Method", state='disabled')
        self.btn_method.place(relx=0.32, rely=0.5)
        self.btn_preps = Button(
            self.root.mainframe, font=intro_font, text="Sample Prepearations", state='disabled')
        self.btn_preps.place(relx=0.45, rely=0.5)
        self.btn_valid = Button(self.root.mainframe, text="Validate Method", font=intro_font, command= self.moveahead)
        self.btn_valid.place(relx=0.65, rely=0.5)
        self.btn_back = Button(self.root.mainframe, text="Back", font=intro_font,
                               command=lambda: IntroScreen(self.root))
        self.btn_back.place(relx=0.85, rely=0.5)
        self.add_features()



class MethodValidationScreen(InputUtils):
    
    def __init__(self,root,settings):
        intro_font = gui_font(letterfont, 10)
        self.root = root
        self.add_features(settings)


    def get_state(settings,statevars):
        Base_Parameters= namedtuple("Base_Parameters",'Curve,Repeatability,Reproducibility')
        to_do=[]
        for i in range(0,9,3):
            if statevars[i] is not None:
                to_do.append(Base_Parameters(Curve=statevars[i].get(),Repeatability=statevars[i+1].get(),Reproducibility=statevars[i+2].get()))
        settings['basic_settings']=to_do
        return defaultdict(lambda:None,settings)

    
    def initiate_validation(root=None,settings=None):
        Validation(root=root,settings=settings)
        return None
    

    
    def modobject(self,atrr=None):
        try:
            if atrr is not None:
                self.atrr =MethodValidationScreen.convert_input(self.atrr)
            else:
                raise KeyValueError
        except KeyValueError:    
            print("Attribute is void!")

    def add_features(self,settings):
        # To implement : R and r are state disabled until curve is checked. Attempt to set these as class vars and have advanced settings inherit them.
        # Very buggy, must fix. 2 state vars are linked in the display and give incorrect values to the user but not the backend.Curve checkboxes appear ticked initially.
        intro_font = gui_font(letterfont, 15)
        var_std = StringVar()
        var_spike = StringVar()
        var_matrix = StringVar()
        var_std_R = BooleanVar()
        var_std_r = BooleanVar()
        var_spike_R = BooleanVar()
        var_spike_r = BooleanVar()
        var_matrix_R = BooleanVar()
        var_matrix_r = BooleanVar()
        var_auto = BooleanVar()
        statevars = [var_std, var_std_R, var_std_r, var_spike, var_spike_R,
                     var_spike_r, var_matrix, var_matrix_R, var_matrix_r, var_auto]
        self.root.mainframe = Frame(self.root, bg='navyblue')
        self.root.mainframe.place(relx=0, rely=0, relheight=1, relwidth=1)
        self.label_title = Label(
            self.root.mainframe, text="Validate Method With:", font=intro_font, bg='blue', padx=50)
        self.label_title.place(relx=0.4, rely=0.1)
        self.chkbtn_std = Checkbutton(self.root.mainframe, text="Standards Curve", font=("Times New Roman", 10),
                                      variable=var_std, onvalue="STD", offvalue=None, bg='blue')
        self.chkbtn_std.place(relx=0.1, rely=0.3)
        self.chkbtn_spike = Checkbutton(self.root.mainframe, text="Spike Curve", font=("Times New Roman", 10),
                                        variable=var_spike, onvalue="Spike", offvalue=None, bg='blue')
        self.chkbtn_spike.place(relx=0.4, rely=0.3)
        self.chkbtn_matrix = Checkbutton(self.root.mainframe, text="Matrix Curve", font=("Times New Roman", 10),
                                         variable=var_matrix, onvalue="Matrix", offvalue=None, bg='blue')
        self.chkbtn_matrix.place(relx=0.7, rely=0.3)
        self.chkbtn_std_R = Checkbutton(self.root.mainframe, text="Reproducibility", font=("Times New Roman", 10),
                                        variable=var_std_R, onvalue=True, offvalue=False, bg='blue')
        self.chkbtn_std_R.place(relx=0.1, rely=0.6)
        self.chkbtn_std_r = Checkbutton(self.root.mainframe, text="Repeatability", font=("Times New Roman", 10),
                                        variable=var_std_r, onvalue=True, offvalue=False, bg='blue')
        self.chkbtn_std_r.place(relx=0.1, rely=0.65)
        self.chkbtn_Spike_R = Checkbutton(self.root.mainframe, text="Reproducibility", font=("Times New Roman", 10),
                                          variable=var_spike_R, onvalue=True, offvalue=False, bg='blue')
        self.chkbtn_Spike_R.place(relx=0.4, rely=0.6)
        self.chkbtn_Spike_r = Checkbutton(self.root.mainframe, text="Repeatability", font=("Times New Roman", 10),
                                          variable=var_spike_r, onvalue=True, offvalue=False, bg='blue')
        self.chkbtn_Spike_r.place(relx=0.4, rely=0.65)
        self.chkbtn_Matrix_R = Checkbutton(self.root.mainframe, text="Reproducibility", font=("Times New Roman", 10),
                                           variable=var_matrix_R, onvalue=True, offvalue=False, bg='blue')
        self.chkbtn_Matrix_R.place(relx=0.7, rely=0.6)
        self.chkbtn_Matrix_r = Checkbutton(self.root.mainframe, text="Repeatability", font=("Times New Roman", 10),
                                           variable=var_matrix_r, onvalue=True, offvalue=False, bg='blue')
        self.chkbtn_Matrix_r.place(relx=0.7, rely=0.65)
        self.chkbtn_auto = Checkbutton(self.root.mainframe, text="Auto Detect Files", font=(
            "Times New Roman", 8), variable=var_auto, onvalue=True, offvalue=False)
        self.chkbtn_auto.place(relx=0.1, rely=0.8)
        ''' project params are duplicated Integrate into a single settings defaultdict'''
        self.btn_ok = Button(self.root.mainframe, text="Ok",
                             font=intro_font, command=lambda: MethodValidationScreen.initiate_validation(root=self.root,settings=MethodValidationScreen.get_state(settings,statevars)))
        self.btn_ok.place(relx=0.1, rely=0.9)
        self.btn_advanced = Button(
            self.root.mainframe, text="Advanced Settings", font=intro_font, command=lambda: MethodValidationSettingsScreen(self.root,MethodValidationScreen.get_state(settings,statevars)))
        self.btn_advanced.place(relx=0.3, rely=0.9)
        self.btn_exit = Button(
            self.root.mainframe, text="Back", font=intro_font, command=self.root.quit)
        self.btn_exit.place(relx=0.5, rely=0.9)
        self.btn_bk = Button(self.root.mainframe, text="Exit",
                             font=intro_font, command=lambda: ProjectTypeScreen(self.r))
        self.btn_bk.place(relx=0.7, rely=0.9)


class MethodValidationSettingsScreen(InputUtils):
    #Make it so it remembers settings when returning from advanced settings
    # windowfont = gui_font(letterfont, 15)

    def __init__(self, root,settings):
        self.root = root
        self.root.geometry("960x750")
        self.add_curve_parameters(settings)

    def initiate_validation(self,settings):
        Validation(root,settings)
    

        # self.curvesformat_fontentry=Entry(self.root.mainframe)
        # self.curvesformat_fontentry.place(relx=.08,rely=c_title_y+.425)
        # self.curvesformat_szentry=Entry(self.root.mainframe)
        # self.curvesformat_szentry.place(relx=.08,rely=c_title_y+.475)
        # self.curvesformat_fontcolorentry=Entry(self.root.mainframe)
        # self.curvesformat_fontcolorentry.place(relx=.08,rely=c_title_y+.45)
        # self.curvesformat_fillentry=Entry(self.root.mainframe)
        # self.curvesformat_fillentry.place(relx=.08,rely=c_title_y+.5)

    def collect_settings(self,settings):
        Format=namedtuple('Format','font,size,font_color,fill')
        settings['advanced_settings']={
        'advanced_curve_settings':{
                    'STD':None,
                    'Spike':None,
                    'Matrix':None
                    
                },
        'format_settings':{
                    'curve_headings':None,
                    'analyte_heading':None,
                    'column_heading':None,
                    'data_headings':None,
                    'sample':None,
                    'blanc':None
                    }
                }

        settings['advanced_settings']['advanced_curve_settings']['STD'] = InputUtils.interpret_input(self.stdcpts.get(),self.stdRlvlsentry.get(),self.stdrlvlsentry.get(),self.stdRrepeatsperlevelentry.get(),self.stdrrepeatsperlevelentry.get())
        settings['advanced_settings']['advanced_curve_settings']['Spike']=InputUtils.interpret_input(self.spikecpts.get(),self.spikeRlvlsentry.get(),self.spikerlvlsentry.get(),self.spikeRrepeatsperlevelentry.get(),self.spikerrepeatsperlevelentry.get())
        settings['advanced_settings']['advanced_curve_settings']['Matrix']=InputUtils.interpret_input(self.matrixcpts.get(),self.matrixRlvlsentry.get(),self.matrixrlvlsentry.get(),self.matrixRrepeatsperlevelentry.get(),self.matrixrrepeatsperlevelentry.get())
        settings['advanced_settings']['format_settings']['curve_heading']=Format(font=self.curvesformat_fontentry.get(),size=self.curvesformat_szentry.get(),font_color=self.curvesformat_fontcolorentry.get(),fill=self.curvesformat_fillentry.get())
        settings['advanced_settings']['format_settings']['analyte_heading']=Format(font=self.analyteformat_fontentry.get(),size=self.analyteformat_szentry.get(),font_color=self.analyteformat_fontcolorentry.get(),fill=self.analyteformat_fillentry.get())
        settings['advanced_settings']['format_settings']['column_heading']=Format(font=self.columnformat_fontentry.get(),size=self.columnformat_szentry.get(),font_color=self.columnformat_fontcolorentry.get(),fill=self.columnformat_fillentry.get())
        settings['advanced_settings']['format_settings']['data_heading']=Format(font=self.dataformat_fontentry.get(),size=self.dataformat_szentry.get(),font_color=self.dataformat_fontcolorentry.get(),fill=self.dataformat_fillentry.get())
        settings['advanced_settings']['format_settings']['sample_heading']=Format(font=self.sampleformat_fontentry.get(),size=self.sampleformat_szentry.get(),font_color=self.sampleformat_fontcolorentry.get(),fill=self.sampleformat_fillentry.get())
        settings['advanced_settings']['format_settings']['blank_heading']=Format(font=self.blankformat_fontentry.get(),size=self.blankformat_szentry.get(),font_color=self.blankformat_fontcolorentry.get(),fill=self.blankformat_fillentry.get())
        return settings



    def add_curve_parameters(self,settings):
        #Adds fields and labels to the screen for curve parameters.
        # stdcpts=StringVar()
        # spikecpts=StringVar()
        # matrixcpts=StringVar()
        # stdRlvlsentry=StringVar()
        # stdRrepeatsperlevelentry=StringVar()
        # stdrlvlsentry=StringVar()
        # stdrrepeatsperlevelentry=StringVar()
        # spikeRlvlsentry=StringVar()
        # spikeRrepeatsperlevelentry=StringVar()
        # spikerlvlsentry=StringVar()
        # spikerrepeatsperlevelentry=StringVar()
        # matrixRlvlsentry=StringVar()
        # matrixRrepeatsperlevelentry=StringVar()
        # matrixrlvlsentry=StringVar()
        # matrixrrepeatsperlevelentry=StringVar()
        c_title_y = 0.15
        self.root.mainframe = Frame(self.root, bg="magenta")
        self.root.mainframe.place(relx=0, rely=0, relwidth=1, relheight=1)
        self.label_title = Label(self.root.mainframe, text="Set Method Validation Parameters:", font=(
            letterfont, 12), bg="magenta")
        self.label_title.place(relx=0.4, rely=0.01)
        self.curvelabelstd = Label(self.root.mainframe, text="STD Curve Parameters", font=(
            letterfont, 11), bg="magenta")
        self.curvelabelstd.place(relx=0.15, rely=c_title_y)
        self.curvelabelspike = Label(self.root.mainframe, text="Spike Curve Parameters", font=(
            letterfont, 11), bg="magenta")
        self.curvelabelspike.place(relx=0.40, rely=c_title_y)
        self.curvelabelmatrix = Label(self.root.mainframe, text="Matrix Match Curve Parameters", font=(
            letterfont, 11), bg="magenta")
        self.curvelabelmatrix.place(relx=0.65, rely=c_title_y)
        self.stdcptsl = Label(self.root.mainframe, text="Point in Curve: ", font=(
            letterfont, 10), bg="magenta")
        self.stdcptsl.place(relx=0.01, rely=c_title_y + 0.1)
        self.spikecptsl = Label(self.root.mainframe, text="Points in Curve", font=(
            letterfont, 10), bg="magenta")
        self.spikecptsl.place(relx=.34, rely=c_title_y + 0.1)
        self.matrixcptsl = Label(self.root.mainframe, text="Points in Curve", font=(
            letterfont, 10), bg="magenta")
        self.matrixcptsl.place(relx=.685, rely=c_title_y + 0.1)
        self.stdcpts = Entry(self.root.mainframe)
        self.stdcpts.place(relx=.11, rely=c_title_y + 0.1)
        self.spikecpts = Entry(self.root.mainframe)
        self.spikecpts.place(
            relx=.5, rely=c_title_y + 0.1)
        self.matrixcpts = Entry(self.root.mainframe)
        self.matrixcpts.place(
            relx=.79, rely=c_title_y + 0.1)
        # STD Labels
        self.stdRlvlslabel = Label(self.root.mainframe, text="Repeatibility Spiking Levels: ", bg="magenta")
        self.stdRlvlslabel.place(relx=.01, rely=c_title_y + 0.134)
        self.stdRrepeatsperlevellabel = Label(
            self.root.mainframe, text="Repeatability repeats per level: ", bg="magenta")
        self.stdRrepeatsperlevellabel.place(relx=.01, rely=c_title_y + 0.168)
        self.stdrlvlslabel = Label(self.root.mainframe, text="Within Laboratory Reproducibility Spiking Levels: ", wraplength=200, bg="magenta")
        self.stdrlvlslabel.place(
            relx=.01, rely=c_title_y + 0.202)
        self.stdrrepeatsperlevellabel = Label(
            self.root.mainframe, text="Within Laboratory Reproducibility Repeats: ", wraplength=200, bg="magenta")
        self.stdrrepeatsperlevellabel.place(relx=.01, rely=c_title_y + .257)
        # Spike Labels
        self.spikeRlvlslabel = Label(self.root.mainframe, text="Repeatibility Spiking Levels: ", bg="magenta")
        self.spikeRlvlslabel.place(
            relx=.35, rely=c_title_y + 0.134)
        self.spikeRrepeatsperlevellabel = Label(
            self.root.mainframe, text="Repeatability repeats per level: ", bg="magenta")
        self.spikeRrepeatsperlevellabel.place(relx=.35, rely=c_title_y + 0.168)
        self.spikerlvlslabel = Label(self.root.mainframe, text="Within Laboratory Reproducibility Spiking Levels: ", bg="magenta", wraplength=200)
        self.spikerlvlslabel.place(
            relx=.35, rely=c_title_y + 0.2)
        self.spikerrepeatsperlevellabel = Label(
            self.root.mainframe, text="Within Laboratory Reproducibility Repeats: ", bg="magenta", wraplength=200)
        self.spikerrepeatsperlevellabel.place(relx=.35, rely=c_title_y + .257)
        # Matrix Labels
        self.matrixRlvlslabel = Label(self.root.mainframe, text="Repeatibility Spiking Levels: ", bg="magenta")
        self.matrixRlvlslabel.place(
            relx=.685, rely=c_title_y + .134)
        self.matrixRrepeatsperlevellabel = Label(
            self.root.mainframe, text="Repeatability repeats per level: ", bg="magenta")
        self.matrixRrepeatsperlevellabel.place(relx=.685, rely=c_title_y + .168)
        self.matrixrlvlslabel = Label(self.root.mainframe, text="Within Laboratory Reproducibility Spiking Levels: ", bg="magenta", wraplength=200)
        self.matrixrlvlslabel.place(
            relx=.685, rely=c_title_y + 0.2)
        self.matrixrrepeatsperlevellabel = Label(
            self.root.mainframe, text="Within Laboratory Reproducibility Repeats: ", bg="magenta", wraplength=200)
        self.matrixrrepeatsperlevellabel.place(relx=.685, rely=c_title_y + .257)
        # STD Entries
        self.stdRlvlsentry = Entry(self.root.mainframe)
        self.stdRlvlsentry.place(
            relx=.18, rely=c_title_y + 0.134)
        self.stdRrepeatsperlevelentry = Entry(
            self.root.mainframe)
        self.stdRrepeatsperlevelentry.place(relx=.195, rely=c_title_y + 0.168)
        self.stdrlvlsentry = Entry(self.root.mainframe)
        self.stdrlvlsentry.place(
            relx=.21, rely=c_title_y + 0.212)
        self.stdrrepeatsperlevelentry = Entry(
            self.root.mainframe)
        self.stdrrepeatsperlevelentry.place(relx=.21, rely=c_title_y + .265)
        # Spike Entries
        self.spikeRlvlsentry = Entry(self.root.mainframe)
        self.spikeRlvlsentry.place(
            relx=.55, rely=c_title_y + 0.134)
        self.spikeRrepeatsperlevelentry = Entry(
            self.root.mainframe)
        self.spikeRrepeatsperlevelentry.place(relx=.55, rely=c_title_y + 0.168)
        self.spikerlvlsentry = Entry(self.root.mainframe)
        self.spikerlvlsentry.place(
            relx=.55, rely=c_title_y + 0.212)
        self.spikerrepeatsperlevelentry = Entry(
            self.root.mainframe)
        self.spikerrepeatsperlevelentry.place(relx=.55, rely=c_title_y + .265)
        # Matrix Entries
        self.matrixRlvlsentry = Entry(self.root.mainframe)
        self.matrixRlvlsentry.place(
            relx=.85, rely=c_title_y + .134)
        self.matrixRrepeatsperlevelentry = Entry(
            self.root.mainframe)
        self.matrixRrepeatsperlevelentry.place(relx=.85, rely=c_title_y + .168)
        self.matrixrlvlsentry = Entry(self.root.mainframe)
        self.matrixrlvlsentry.place(
            relx=.877, rely=c_title_y + 0.2)
        self.matrixrrepeatsperlevelentry = Entry(
            self.root.mainframe)
        self.matrixrrepeatsperlevelentry.place(relx=.877, rely=c_title_y + .257)
        self.add_results_format(c_title_y,settings)
    
    def add_results_format(self,c_title_y,settings):
    #Adds Results Format options
        self.resultsformat = Label(self.root.mainframe, text = "Results Format",font =(letterfont,12),bg='magenta')
        self.resultsformat.place(relx=.4,rely=c_title_y + .35)
    #Curve Heading
        self.curvesformat_heading = Label(self.root.mainframe, text = "Curve Heading:",font=(letterfont,11),bg='magenta')
        self.curvesformat_heading.place(relx=.088,rely=c_title_y+.385)
        self.curvesformat_font=Label(self.root.mainframe,text="Font:",font =(letterfont,12),bg='magenta')
        self.curvesformat_font.place(relx=0,rely=c_title_y+.425)
        self.curvesformat_sz=Label(self.root.mainframe,text="Size:",font =(letterfont,12),bg='magenta')
        self.curvesformat_sz.place(relx=0,rely=c_title_y+.45)
        self.curvesformat_fontcolor=Label(self.root.mainframe,text="Font Color:",font =(letterfont,12),bg='magenta')
        self.curvesformat_fontcolor.place(relx=0,rely=c_title_y+.475)
        self.curvesformat_fill=Label(self.root.mainframe,text="Fill:",font =(letterfont,12),bg='magenta')
        self.curvesformat_fill.place(relx=0,rely=c_title_y+.5)
    #Curve Entries
        self.curvesformat_fontentry=Entry(self.root.mainframe)
        self.curvesformat_fontentry.place(relx=.08,rely=c_title_y+.425)
        self.curvesformat_szentry=Entry(self.root.mainframe)
        self.curvesformat_szentry.place(relx=.08,rely=c_title_y+.45)
        self.curvesformat_fontcolorentry=Entry(self.root.mainframe)
        self.curvesformat_fontcolorentry.place(relx=.08,rely=c_title_y+.475)
        self.curvesformat_fillentry=Entry(self.root.mainframe)
        self.curvesformat_fillentry.place(relx=.08,rely=c_title_y+.5)
    #Analyte Heading
        self.analyteformat_heading = Label(self.root.mainframe, text = "Analyte Heading:",font=(letterfont,11),bg='magenta')
        self.analyteformat_heading.place(relx=.288,rely=c_title_y+.385)
        self.analyteformat_font=Label(self.root.mainframe,text="Font:",font =(letterfont,12),bg='magenta')
        self.analyteformat_font.place(relx=.2,rely=c_title_y+.425)
        self.analyteformat_sz=Label(self.root.mainframe,text="Size:",font =(letterfont,12),bg='magenta')
        self.analyteformat_sz.place(relx=.2,rely=c_title_y+.45)
        self.analyteformat_fontcolor=Label(self.root.mainframe,text="Font Color:",font =(letterfont,12),bg='magenta')
        self.analyteformat_fontcolor.place(relx=.2,rely=c_title_y+.475)
        self.analyteformat_fill=Label(self.root.mainframe,text="Fill:",font =(letterfont,12),bg='magenta')
        self.analyteformat_fill.place(relx=.2,rely=c_title_y+.5)
    #Analyte Entry
        self.analyteformat_fontentry=Entry(self.root.mainframe)
        self.analyteformat_fontentry.place(relx=.28,rely=c_title_y+.425)
        self.analyteformat_szentry=Entry(self.root.mainframe)
        self.curvesformat_szentry.place(relx=.28,rely=c_title_y+.45)
        self.analyteformat_fontcolorentry=Entry(self.root.mainframe)
        self.analyteformat_fontcolorentry.place(relx=.28,rely=c_title_y+.475)
        self.analyteformat_fillentry=Entry(self.root.mainframe)
        self.analyteformat_fillentry.place(relx=.28,rely=c_title_y+.5)
    #Column Heading
        self.columnformat_heading = Label(self.root.mainframe, text = "Column Heading:",font=(letterfont,11),bg='magenta')
        self.columnformat_heading.place(relx=.488,rely=c_title_y+.385)
        self.columnformat_font=Label(self.root.mainframe,text="Font:",font =(letterfont,12),bg='magenta')
        self.columnformat_font.place(relx=.4,rely=c_title_y+.425)
        self.columnformat_sz=Label(self.root.mainframe,text="Size:",font =(letterfont,12),bg='magenta')
        self.columnformat_sz.place(relx=.4,rely=c_title_y+.45)
        self.columnformat_fontcolor=Label(self.root.mainframe,text="Font Color:",font =(letterfont,12),bg='magenta')
        self.columnformat_fontcolor.place(relx=.4,rely=c_title_y+.475)
        self.columnformat_fill=Label(self.root.mainframe,text="Fill:",font =(letterfont,12),bg='magenta')
        self.columnformat_fill.place(relx=.4,rely=c_title_y+.5)
    #Column Entry
        self.columnformat_fontentry=Entry(self.root.mainframe)
        self.columnformat_fontentry.place(relx=.48,rely=c_title_y+.425)
        self.columnformat_szentry=Entry(self.root.mainframe)
        self.columnformat_szentry.place(relx=.48,rely=c_title_y+.45)
        self.columnformat_fontcolorentry=Entry(self.root.mainframe)
        self.columnformat_fontcolorentry.place(relx=.48,rely=c_title_y+.475)
        self.columnformat_fillentry=Entry(self.root.mainframe)
        self.columnformat_fillentry.place(relx=.48,rely=c_title_y+.5)
    #Data Heading
        self.dataformat_heading = Label(self.root.mainframe, text = "Data Heading:",font=(letterfont,11),bg='magenta')
        self.dataformat_heading.place(relx=.688,rely=c_title_y+.385)
        self.dataformat_font=Label(self.root.mainframe,text="Font:",font =(letterfont,12),bg='magenta')
        self.dataformat_font.place(relx=.6,rely=c_title_y+.425)
        self.dataformat_sz=Label(self.root.mainframe,text="Size:",font =(letterfont,12),bg='magenta')
        self.dataformat_sz.place(relx=.6,rely=c_title_y+.45)
        self.dataformat_fontcolor=Label(self.root.mainframe,text="Font Color:",font =(letterfont,12),bg='magenta')
        self.dataformat_fontcolor.place(relx=.6,rely=c_title_y+.475)
        self.dataformat_fill=Label(self.root.mainframe,text="Fill:",font =(letterfont,12),bg='magenta')
        self.dataformat_fill.place(relx=.6,rely=c_title_y+.5)
    #Data Entry
        self.dataformat_fontentry=Entry(self.root.mainframe)
        self.dataformat_fontentry.place(relx=.68,rely=c_title_y+.425)
        self.dataformat_szentry=Entry(self.root.mainframe)
        self.dataformat_szentry.place(relx=.68,rely=c_title_y+.45)
        self.dataformat_fontcolorentry=Entry(self.root.mainframe)
        self.dataformat_fontcolorentry.place(relx=.68,rely=c_title_y+.475)
        self.dataformat_fillentry=Entry(self.root.mainframe)
        self.dataformat_fillentry.place(relx=.68,rely=c_title_y+.5)
    #Sample Heading
        self.sampleformat_heading = Label(self.root.mainframe, text = "Sample & Blank Heading:",font=(letterfont,11),bg='magenta')
        self.sampleformat_heading.place(relx=.888,rely=c_title_y+.385)
        self.sampleformat_font=Label(self.root.mainframe,text="Font:",font =(letterfont,12),bg='magenta')
        self.sampleformat_font.place(relx=.8,rely=c_title_y+.425)
        self.sampleformat_sz=Label(self.root.mainframe,text="Size:",font =(letterfont,12),bg='magenta')
        self.sampleformat_sz.place(relx=.8,rely=c_title_y+.45)
        self.sampleformat_fontcolor=Label(self.root.mainframe,text="Font Color:",font =(letterfont,12),bg='magenta')
        self.sampleformat_fontcolor.place(relx=.8,rely=c_title_y+.475)
        self.sampleformat_fill=Label(self.root.mainframe,text="Fill:",font =(letterfont,12),bg='magenta')
        self.sampleformat_fill.place(relx=.8,rely=c_title_y+.5)
    #Sample Entry
        self.sampleformat_fontentry=Entry(self.root.mainframe)
        self.sampleformat_fontentry.place(relx=.88,rely=c_title_y+.425)
        self.sampleformat_szentry=Entry(self.root.mainframe)
        self.sampleformat_szentry.place(relx=.88,rely=c_title_y+.45)
        self.sampleformat_fontcolorentry=Entry(self.root.mainframe)
        self.sampleformat_fontcolorentry.place(relx=.88,rely=c_title_y+.475)
        self.sampleformat_fillentry=Entry(self.root.mainframe)
        self.sampleformat_fillentry.place(relx=.88,rely=c_title_y+.5)
    #Blank Heading
        self.blankformat_heading = Label(self.root.mainframe, text = "Sample & Blank Heading:",font=(letterfont,11),bg='magenta')
        self.blankformat_heading.place(relx=.888,rely=c_title_y+.385)
        self.blankformat_font=Label(self.root.mainframe,text="Font:",font =(letterfont,12),bg='magenta')
        self.blankformat_font.place(relx=.8,rely=c_title_y+.425)
        self.blankformat_sz=Label(self.root.mainframe,text="Size:",font =(letterfont,12),bg='magenta')
        self.blankformat_sz.place(relx=.8,rely=c_title_y+.45)
        self.blankformat_fontcolor=Label(self.root.mainframe,text="Font Color:",font =(letterfont,12),bg='magenta')
        self.blankformat_fontcolor.place(relx=.8,rely=c_title_y+.475)
        self.blankformat_fill=Label(self.root.mainframe,text="Fill:",font =(letterfont,12),bg='magenta')
        self.blankformat_fill.place(relx=.8,rely=c_title_y+.5)
    #Blank Entry
        self.blankformat_fontentry=Entry(self.root.mainframe)
        self.blankformat_fontentry.place(relx=.88,rely=c_title_y+.425)
        self.blankformat_szentry=Entry(self.root.mainframe)
        self.blankformat_szentry.place(relx=.88,rely=c_title_y+.45)
        self.blankformat_fontcolorentry=Entry(self.root.mainframe)
        self.blankformat_fontcolorentry.place(relx=.88,rely=c_title_y+.475)
        self.blankformat_fillentry=Entry(self.root.mainframe)
        self.blankformat_fillentry.place(relx=.88,rely=c_title_y+.5)
    #Buttons
        self.btn_ok=Button(self.root.mainframe,text="Ok",font=(letterfont,12),command=lambda: Validation(settings=self.collect_settings(settings),root=self.root),padx=10)
        self.btn_ok.place(relx=.15,rely=c_title_y+.65)
        self.btn_cnl=Button(self.root.mainframe,text="Cancel",font=(letterfont,12),command=self.root.quit)
        self.btn_cnl.place(relx=.35,rely=c_title_y+.65)
        self.btn_sv=Button(self.root.mainframe,text="Save",font=(letterfont,12),command=lambda: Validation.Save(settings=self.collect_settings(settings),filepath=settings['project_parameters']['filepath']))
        self.btn_sv.place(relx=.55,rely=c_title_y+.65)
        self.btn_ext=Button(self.root.mainframe,text="Exit",font=(letterfont,12),command=self.root.quit)
        self.btn_ext.place(relx=.75,rely=c_title_y+.65)




class ErrorScreen:
    pass


class WarningScreen:
    pass


def gui_main():
        # Weird namespace issue with screen. Hardcode now, implement later
    global debugging
    global screen
    global gui_font
    global letterfont
    debugging = True
    letterfont = "Times New Roman"
    root = Tk()
    root.title('Project name placeholder')
    gui_font = namedtuple("gui_font", ['font', 'size'])
    window = IntroScreen(root)
    mainloop()
    return gui_main


def main():
    gui_main()
    return main


if __name__ == '__main__':
    main()
