import PySimpleGUI as sg


def add_pool(pool_num, window : sg.Window = None):
    
    tab_layout = [[sg.T("How large is the pool?"), sg.In(k=('-SIZE-', pool_num), size = 7, justification="center")],
                    [sg.T("What number is in the pool?"), sg.In(k=('-NUM-', pool_num), size = 7, justification="center") if window == None or not window.key_dict.__contains__(('-NUM-', pool_num)) else window[('-NUM-', pool_num)]],
                    [sg.B("Add a Pool", k=('-ADD-POOL-', pool_num))]]
    
    if pool_num != 1:
        tab_layout.append([sg.B("Delete This Pool", k=('-DEL-', pool_num))])
        
    tab = sg.Tab("Pool " + str(pool_num), tab_layout, k=('-POOL-', pool_num))
    
    return [[tab]]

def add_result(result_num):
    
    result_layout = sg.Col([[sg.T('________', k=('-RESULT-NUM-', result_num))], 
                            [sg.In(f"Result {result_num}", k=('-RESULT-NAME-', result_num), size = 10, justification="center")]], 
                           element_justification='center', k=('-RESULT-', result_num))
    result_col = sg.Col([[result_layout, sg.VerticalSeparator()]], k=('-RESULT-COL-', result_num), justification="left", vertical_alignment='top')
    return [[result_col]]

# All the stuff inside your window.
def make_window():
    pool_num = 1
    
    tab_layout = [[sg.T("How large is the pool?"), sg.In(k=('-SIZE-', pool_num), size = 7, justification="center")],
                    [sg.T("What number is in the pool?"), sg.In(k=('-NUM-', pool_num), size = 7, justification="center")],
                    [sg.B("Add a Pool", k=('-ADD-POOL-', pool_num))]]
    
    limit_layout = [[sg.T("Sum Maximum"), sg.In(k='-MAX-', size = 7, justification="center")],
                    [sg.T("Sum Minimum"), sg.In(k='-MIN-', size = 7, justification="center")]]
    
    layout = [[sg.TabGroup(add_pool(1), k='-POOLS-'),
               sg.Frame("Limits", limit_layout)], 
              [sg.Frame("Results", [[sg.Col(add_result(1), k='-RESULTS-INNER-')], [sg.Col([[sg.B("+",k="-ADD-RESULT-")], [sg.B("-",k="-DEL-RESULT-", visible=False)]], k='-RESULTS-CHANGE-COL-')]], k='-RESULTS-', element_justification="left", expand_x=True)]]

    # Create the Window
    window = sg.Window('Hello Example', layout, element_justification='center')

    return window

def main():

    window = make_window()
    tab_group: sg.TabGroup = window['-POOLS-']
    tab_count = 1
    result_count = 1

    while True:
        event, values = window.read()
        
        print(event, values)
        if event == sg.WIN_CLOSED or event == 'Exit':
            break
        if event[0] == '-ADD-POOL-':
            if tab_group.find_key_from_tab_name("Pool " + str(tab_count + 1)) != None:
                window[('-POOL-', tab_count + 1)].update(visible=True)
            else:
                tab_group.add_tab(add_pool(tab_count + 1, window))

            tab_count += 1

            window[('-POOL-', tab_count)].select()
            window.refresh()
            
        if event[0] == '-DEL-':
            window[tab_group.find_key_from_tab_name("Pool " + str(tab_count))].update(visible=False)
            tab_count -= 1
            window.refresh()
            
        if event == '-ADD-RESULT-':
            if window.key_dict.__contains__(('-RESULT-COL-', result_count + 1)):
                window[('-RESULT-COL-', result_count + 1)].update(visible=True)
            else:
                window.extend_layout(window['-RESULTS-INNER-'], add_result(result_count + 1))

            if result_count == 1:
                window['-DEL-RESULT-'].update(visible=True)

            result_count += 1
            window.refresh()
        if event == '-DEL-RESULT-' and result_count != 1:
            window[('-RESULT-COL-', result_count)].update(visible=False)
            result_count -= 1

            if result_count == 1:
                window['-DEL-RESULT-'].update(visible=False)
            
            window.refresh()
              
    window.close()

if __name__ == '__main__':
    main()


