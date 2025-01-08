import gradio
import requests
import pandas as pd
import os
from datetime import datetime
import json

service_ip = "*****"
service_port = 111

def update_node_info():
    # data = np.random.randint(1, 101, size=(5, 5))  # 随机生成5行3列的整数数据
    data = {
        "*******************************"
        }
    response = requests.get('http://%s:%d/..'%(service_ip, service_port), params=data)
    nodes = response.json()
    def path_to_image_html(path):
        return f'<img src="{path}" />' #style="width:50%; height:auto;"  
    # print(nodes)
    if len(nodes) > 0:
        data_disp = []
        for i_data in nodes:
            data_disp.append([i_data["id"],
                              i_data["name"],
                              i_data["description"],
                              i_data["parent"],
                              i_data["price"],
                              i_data["gender"],
                              i_data["video_length"],
                              i_data["frame_num"],
                              i_data["preview"][0]
                              ])

        df   = pd.DataFrame(data_disp, columns=["ID", "名称", "描述", "所属", "价格(元)","性别","时长(秒)","帧数","预览"])
        html = df.to_html(escape=False, formatters={"预览": path_to_image_html}) # 把指定的内容HTML化
    html_table = f"""
        <style>
            table {{
                width: 100%;
                border-collapse: collapse;
            }}
            th, td {{
                padding: 8px;
                text-align: left;
                border: 1px solid #ddd;
            }}
            td:last-child {{
                width: 50%;  /* 设置最后一列的宽度为33% */
            }}
            img {{
                display: block;
                margin: 0 auto;
            }}
        </style>
        {html}
        """
    return html_table

# 第一界面的函数，提交更新视频模版
def invoke_update(a):
    pass

# 更新模版的过程中需要打印出处理结果的json信息
def upload_template(video_template):
    # save the video template model
    temp_file_path = video_template.name
    temp_dir = "temp"
    os.makedirs(temp_dir, exist_ok=True)
    timestamp = datetime.now().strftime("%Y-%m-%d--%H-%M-%S")
    with open(temp_file_path, 'rb') as file_obj:
        out_file_path = os.path.join(temp_dir, f"{timestamp}_template.mp4")
        with open(out_file_path, "wb") as f:
            f.write(file_obj.read())
    # pass the video path to specific function
    # =========================================
    result_json    = invoke_update(out_file_path)
    formatted_json = format_json(result_json)
    # =========================================
    print(f"upload successfully {video_template}")
    return formatted_json

# 对返回的json进行格式化的输出
def format_json(input_json):
    try:
        json_obj = json.loads(input_json)
        formatted_json = json.dumps(json_obj, indent=4)
        return formatted_json
    except json.JSONDecodeError:
        return "输入的字符串不是有效的JSON格式。", ""

# 第二个界面的函数，调用提交CAT
def invoke_CAT(a,b,c,d):
    print(a,b,c,d)
    pass

# 第二个界面的查询函数，根据输入的模版名称更新下拉选框的值
def search_parent_cat_from_database():
    new_choice = ["1"]
    return new_choice

def search_sub_cat_from_database():
    new_choice = ["1"]
    return new_choice

# 第三个界面的函数，根据数据库查询的结果得到子模版的下拉选框的值
def search_for_subItem_from_database():
    new_choice = ["1"]
    return new_choice

# 第二个界面从数据库获取cat信息
# input templatename get CAT info from server and present in DropDown item
def get_cat_parent_from_database(template_name):
    print("invoke cat_parent_data")
    # =================
    # invoke the search function, return the value
    return_choices = search_parent_cat_from_database()
    # =================
    choices = return_choices
    return gradio.Dropdown(choices=choices, interactive=True)

def get_cat_sub_from_database():
    print("invoke cat_sub_data")
    # =================
    # invoke the search function, return the value
    return_choices = search_sub_cat_from_database()
    # =================
    choices = return_choices
    return gradio.Dropdown(choices=choices, interactive=True)

# 第三个界面，提交parentItem到后台数据
def invoke_submit_parent(parentItem, parentDesc):
    print("invoke submit parentItem func")
    pass

# 第三个界面，提交subItem到后台数据
def invoke_submit_sub(subItem, subDesc):
    print("invoke submit subItem func")
    pass

# 第三个界面，从数据库获取subItem
def get_sub_item_from_database():
    print("invoke the func to get subItem")
    return_choices = search_for_subItem_from_database()
    # =================
    choices = return_choices
    return gradio.Dropdown(choices=choices, interactive=True)

with gradio.Blocks() as demo:
    with gradio.Tabs():
        with gradio.TabItem("上传模版视频"):
            upload    = gradio.File(label="请选择你的视频模版文件")
            jsonOut   = gradio.Code(label="返回的信息", language="json")
            submitBtn = gradio.Button("点击开始处理")
            submitBtn.click(fn=upload_template, inputs=upload, outputs=jsonOut)
        
        with gradio.TabItem("插入模版"):
            template_name = gradio.Textbox(label="视频模版名称", lines=1)
            description   = gradio.Textbox(label="视频模版描述", lines=1)
            choices       = []
            parent_class  = gradio.Dropdown(label="选择一个模版大类", choices=choices)
            
            # 点击选择的时候，会更新选择框的值
            parent_class.focus(get_cat_parent_from_database, [template_name], parent_class)   
            sub_class     = gradio.Dropdown(label="选择一个模版子类", choices=choices)
            sub_class.focus(get_cat_sub_from_database, [], sub_class)

            cat_button    = gradio.Button("提交模版")
            cat_info      = gradio.Textbox(label="任务状态")
            cat_button.click(fn=invoke_CAT, 
                             inputs=[template_name, description, parent_class, sub_class], 
                             outputs=cat_info
                             )
        
        with gradio.TabItem("添加模版类别"):
            with gradio.Row():
                with gradio.Column():
                    parent_item     = gradio.Textbox(label = "添加大类名称", lines=1)
                    parent_descript = gradio.Textbox(label = "添加大类描述", lines=1)
                    parentBtn       = gradio.Button("点击插入大类")
                    parent_return   = gradio.Textbox(label = "插入父类进程状态")
                with gradio.Column():
                    choices      = []
                    sub_item     = gradio.Dropdown(label = "选择一个大类", choices=choices)
                    sub_descript = gradio.Textbox(label  = "添加子类名称", lines=1)
                    sub_descript = gradio.Textbox(label  = "添加子类描述", lines=1)
                    sub_return   = gradio.Textbox(label  = "插入子类进程的状态")
                    subBtn       = gradio.Button("点击提交子类")
            sub_item.focus(get_sub_item_from_database,[], [sub_item])
            parentBtn.click(fn=invoke_submit_parent,
                            inputs=[parent_item, parent_descript],
                            outputs=[parent_return])
            subBtn.click(fn=invoke_submit_sub,
                         inputs=[sub_item, sub_descript],
                         outputs=[sub_return])
        
        with gradio.TabItem("模板管理"):
            with gradio.Row():
                node_info = gradio.HTML(label='已知模板情况', value=update_node_info())
            with gradio.Row():
                with gradio.Column():
                    run_btn = gradio.Button("查询模板情况", elem_id="run-btn")
            
            run_btn.click(
                fn = update_node_info,
                outputs = node_info
            )
demo.launch()
