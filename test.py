# Add button in QtableWidget
# test
        # self.tableWidget_2.itemDoubleClicked.connect(self.prt)
        table = self.tableWidget_3

        # create an item
        item = QTableWidgetItem('save')
        item2 = QTableWidgetItem('Asave')
        Tools.insertNewRow(table,0)
        table.setItem(0, 4, item)
        table.setItem(0, 3, item2)

        # or specifically for this item
        item.setFlags( item.flags() ^ Qt.ItemIsEditable)
        
        # create a connection to the double click event
        table.itemDoubleClicked.connect(self.prt)
        
        # Button.
        Tools.insertNewRow(table,1)
        for i in range(2):

            editBtn = QPushButton(table)
            delBtn = QPushButton(table)

            editBtn.setText("Edit")
            delBtn.setText("Del")
            a = QDialogButtonBox(table)
            
            editBtn.clicked.connect(self.prt)
            delBtn.clicked.connect(self.prt)
            
            # Btns = QHBoxLayout()
            # Btns.addWidget(editBtn)
            # Btns.addChildWidget(Btns, delBtn)
            
            
            table.setCellWidget(i,2,self.buttonBox)
        # table.setItem(1,2 ,item)
        # table.setCellWidget(1,2,self.pushButton_18)

        # if you don't want to allow in-table editing, either disable the table like:
        table.setEditTriggers( QTableWidget.NoEditTriggers )









# Add Button to table widget.
# test
        table = self.tableWidget_3


        for i in range(3):
            Tools.insertNewRow(table, i)

            btn = QDialogButtonBox(table)

            btn.setStyleSheet("width:200px; font-size:10pt;")


            btn.addButton('Edit',btn.AcceptRole)
            btn.addButton('Del',btn.HelpRole)

            btn.accepted.connect(self.prt)
            btn.helpRequested.connect(self.prt2)
            
            table.setCellWidget(i,2, btn)
        