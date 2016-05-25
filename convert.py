
#-*- coding: utf-8 -*-  

""" 信息转换类
  
    *----- 字典与字符串转换-----*

    * 1.mqtt字符串报文转换为字典*

    * 2.字典信息桩换为mqtt字符串*

    *-----       结束      -----*

"""

import errno
from conf import *

# 消息转换类状态定义

MSG_D2S = 0    # 字典形式转字符串
MSG_S2D = 1    # 字符串形式转字典
MSG_ERR = 2    # 消息类型错误

class MsgConv(object):
    """ 消息桩换类
    """

    def __init__(self, msg=None, mid=''):
        """ 初始化函数,传入待转换消息
        """
        if type(msg) is str:
            self._state = MSG_S2D
        elif type(msg) is dict:
            self._state = MSG_D2S
            id_list = ['27','29','2B','2D','2F','30','40','42','44','46','49','4A']
            if mid not in id_list:
                print 'dict对应id非法' 
        else:
            self._state = MSG_ERR

        self._mid = mid       # d2s时需指定id参数
        self._msg = msg
        self._mdata = ''       # 消息真实数据

        self._d2s_func_dict = {'27':self._set_time,     #  后台与桩对时  
                               '29':self._get_info,     #  请求桩基本信息
                               '2B':self._get_data,     #  获取桩实时数据
                               '2D':self._get_log,      #  获取桩实时充电纪录
                               '2F':self._log_ack,      #  应答桩上传充电纪录
                               '30':self._get_code,     #  请求充电验证码
                               '40':self._start_ctrl,   #  控制桩启停
                               '42':self._set_pwm,      #  设置桩pwm
                               '44':self._remote_start, #  远程控制桩开关机
                               '46':self._set_pile,     #  更改模块桩编号
                               '49':self._rmrst_ack,    #  应答桩上传远程开关机结果
                               '4A':self._get_state     #
        }
        
        self._s2d_func_dict = {'20':self._up_info,      #  桩上传设备基本信息
                               '28':self._up_state,     #  桩上传接口实时状态
                               '2A':self._up_sreason,   #  停机时候桩上传停机原因
                               '2C':self._up_data,      #  桩上传实时数据
                               '2E':self._up_log,       #  桩上传充电纪录
                               '31':self._up_req,       #  桩上传请求充电状态
                               '41':self._start_ack,    #  桩回复启停操作
                               '43':self._pwm_ack,      #  桩回复pwm设置操作
                               '45':self._remt_ack,     #  桩回复远程开关机操作
                               '47':self._set_ack,      #  模块回复更改桩编号
                               '48':self._remt_rst,     #  桩上传远程开关机结果 
        }

    def _msg_check(self):
        """ 帧合法性检测函数,正确保存id,与数据部分
        """
        if self._state == MSG_ERR:
            print '消息类型错误'
            return False

        data = self._msg

        try:
            head_pos = data.index('68')
        except:
            return False

        asdu_len = int(eval('0x'+data[head_pos+2:head_pos+4]))
        data_id = data[head_pos+4:head_pos+6]  # 16进制字符串类型帧ID

        # 判断结束信息0x16
        rear_pos = head_pos+2*asdu_len+2     # 报文尾位置
        if not data[rear_pos:rear_pos+2] == '16':
            return False
        # 判断检验结果
        if not int(eval('0x'+data[head_pos+2*asdu_len:head_pos+2*asdu_len+2])) == asdu_len-2:
            return False

        self._mid = data_id
        self._mdata = data[head_pos+6:rear_pos-2]

        return True
    
    def _pack_single_str(self,dlen,data):
        """ 将单个组装成报文字符串
        """
        ori_str = str(hex(data))[2:]

        if not (len(ori_str)%2 == 0):
            ori_str = '0' + ori_str
        str1 = '0'*(dlen-len(ori_str)) + ori_str

        return str1

    def _pack_full_str(self,data=''):
        """ 组装完成报文字符串
        """
        dlen = len(data)/2
        str1 = str(hex(dlen+3))[2:]

        if not (len(str1)%2 == 0):
            str1 = '0' + str1

        head = '68'+str1+self._mid
        str2 = str(hex(dlen+1))[2:]

        if not (len(str2)%2 == 0):
            str2 = '0' + str2

        rear = str2+ '16'

        return head + data + rear
    
    # 字典转字符串操作函数
    def _set_time(self):
        """ 后台与桩对时
        """
        info = self._msg
        str1 = self._pack_single_str(32,(int)(info['pile_code']))
        str2 = self._pack_single_str(14,info['time'])
        return self._pack_full_str(str1+str2)
    
    def _get_info(self):
        """
        """
    def _get_data(self):
        """
        """
    def _get_log(self):
        """
        """
    def _log_ack(self):
        """
        """
    def _get_code(self):
        """
        """
    def _start_ctrl(self):
        """
        """
        info = self._msg
        str1 = '0'*16+info['pile_code']
        str2 = self._pack_single_str(20,info['user_id'])
        str3 = self._pack_single_str(2,info['start_state'])
        str4 = self._pack_single_str(2,info['charge_port'])

        return self._pack_full_str(str1+str2+str3+str4)
    
    def _set_pwm(self):
        """
        """
    def _remote_start(self):
        """
        """
    def _set_pile(self):
        """
        """
    def _rmrst_ack(self):
        """
        """
    def _get_state(self):
        """
        """
    
    # 字符串转字典操作函数
    def _up_info(self):
        """ 桩上传基本信息
        """
        data = self._mdata
        info_dict = {}
        info_dict['pile_code'] = self._pack_single_str(16,eval('0x'+data[0:32]))               # 16位桩ID
        info_dict['charge_port'] = eval('0x'+data[32:34]) # 充电接口
        info_dict['dev_state'] = eval('0x'+data[34:36])   # 设备运行状态
        info_dict['port_num']  = eval('0x'+data[36:38])   # 充电接口个数
        info_dict['meter_num']  = eval('0x'+data[38:40])  # 电表个数

        return info_dict
    
    def _up_state(self):
        """ 桩上传实时状态
        """
        data = self._mdata
        info_dict = {}
        info_dict['pile_code'] = self._pack_single_str(16,eval('0x'+data[0:32]))               # 16位桩ID
        info_dict['inter_no'] = eval('0x'+data[32:34]) # 充电接口
        info_dict['inter_type'] = eval('0x'+data[34:36])   # 接口类型:直流OR交流
        info_dict['inter_conn_state'] = eval('0x'+data[36:38])     # 连接状态:车连接...
        info_dict['inter_work_state'] = eval('0x'+data[38:40])     # 充电,待机，随意...
        info_dict['inter_order_state'] = eval('0x'+data[40:42])   # 充电接口预约状态
        info_dict['meter_type']  = eval('0x'+data[42:44])    # 电表类型
        info_dict['meter_addr'] = eval(data[44:68])          # 电表地址
        info_dict['meter_rate'] = eval('0x'+data[68:76])     # 电表倍率
        info_dict['meter_active_power'] = eval('0x'+data[76:80])*POWER_SCALE_FACTOR # 电表有功功率
        info_dict['meter_reactive_power'] = eval('0x'+data[80:84])*POWER_SCALE_FACTOR #电表无功功率
        info_dict['meter_active_energy'] = eval('0x'+data[84:88])*ELEC_DEGREE_FACTOR # 电表有功电能
        info_dict['meter_reactive_energy'] = eval('0x'+data[88:92])*ELEC_DEGREE_FACTOR #电表无功电能
        info_dict['voltage'] = eval('0x'+data[92:96])*VOLTAGE_SCALE_FACTOR # 输出电压
        info_dict['current'] = (eval('0x'+data[96:100])-CURR_OFFSET)*CURR_SCALE_FACTOR # 输出电流
        info_dict['input_a_vol'] = eval('0x'+data[100:104])*VOLTAGE_SCALE_FACTOR # 输入a相电压
        info_dict['input_b_vol'] = eval('0x'+data[104:108])*VOLTAGE_SCALE_FACTOR # 输入b相电压
        info_dict['input_c_vol'] = eval('0x'+data[108:112])*VOLTAGE_SCALE_FACTOR # 输入c相电压
        info_dict['input_a_cur'] = (eval('0x'+data[112:116])-CURR_OFFSET)*CURR_SCALE_FACTOR # 输入a相电流
        info_dict['input_b_cur'] = (eval('0x'+data[116:120])-CURR_OFFSET)*CURR_SCALE_FACTOR # 输入b相电流
        info_dict['input_c_cur'] = (eval('0x'+data[120:124])-CURR_OFFSET)*CURR_SCALE_FACTOR # 输入c相电流
        info_dict['fault_code'] = eval('0x'+data[124:126])  # 故障代码
        info_dict['errocode'] = eval('0x'+data[126:128])    # 错误代码
        info_dict['curr_soc'] = eval('0x'+data[128:130])    # 当前soc
        info_dict['remain_time'] = eval('0x'+data[130:132]) # 充电剩余时间
        
        return info_dict
    
    def _up_sreason(self):
        """ 桩上传停机原因
        """
        data = self._mdata
        info_dict = {}
        info_dict['pile_code'] = data[0:32]                # 桩16位编码
        info_dict['charge_port'] = eval('0x'+data[32:34])  # 充电接口
        info_dict['stop_reson'] = eval('0x'+data[34:36])   # 停机原因
        info_dict['card_num'] = eval(data[36:68])          # 卡号
        info_dict['total_energy'] =  eval('0x'+data[68:72])*ELEC_DEGREE_FACTOR  # 充电总电量
        info_dict['total_time'] = eval('0x'+data[72:76])   # 总时间
        info_dict['close_time'] = eval('0x'+data[76:90])   # 停机时间

        return info_dict
    
    def _up_data(self):
        """ 桩上传实时数据
        """
        data = self._mdata
        info_dict = {}
        info_dict['pile_code'] = data[0:32]            # 桩16位编码
        info_dict['session_id'] = eval('0x'+data[32:40])   # 会话ID
        info_dict['charge_port'] = eval('0x'+data[40:42])  # 充电接口
        info_dict['card_num'] = data[42:74]          # 卡号
        info_dict['cur_charge_money'] = eval('0x'+data[74:82])*0.01  # 充电金额
        info_dict['cur_charge_energy'] = eval('0x'+data[82:90])*0.01 # 充电电量
        info_dict['cur_charge_time'] = eval('0x'+data[90:98])        # 充电时间
        info_dict['cur_soc'] = eval('0x'+data[98:100])               # 剩余soc

        return info_dict
    
    def _up_log(self):
        """ 桩上传日志纪录(有卡,保留)
        """
    def _up_req(self):
        """ 桩上传请求充电状态
        """
        data = self._mdata
        info_dict = {}
        info_dict['pile_code'] = data[0:32]                # 16位桩编码
        info_dict['charge_port'] = eval('0x'+data[32:34])  # 充电接口编号
        info_dict['user_id'] = eval(data[34:66])           # 16位用户ID
        info_dict['task_serial'] = eval(data[66:90])       # 业务流水号
        info_dict['req_state'] = eval(data[90:92])         # 请求状态
        info_dict['reserved'] = ''                         # 保留字段
        
        return info_dict
        
    def _start_ack(self):
        """ 桩回复启停操作
        """
        data = self._mdata
        info_dict = {}
        info_dict['pile_code'] = self._pack_single_str(16,eval('0x'+data[0:32]))               # 16位桩ID
        info_dict['user_id'] = eval('0x'+data[32:52])     # 10位用户ID
        info_dict['opr_type'] = eval('0x'+data[52:56])    # 操作类型：关机或者开机
        info_dict['charge_port'] = eval('0x'+data[56:60]) # 充电接口
        info_dict['opr_state'] = eval('0x'+data[60:62])   # 操作结果
        
        return info_dict

    def _pwm_ack(self):
        """ 桩回复pwm设置操作
        """
        data = self._mdata
        info_dict = {}
        info_dict['pile_code']= data[0:32] 
        info_dict['power_limit'] = eval('0x'+data[32:34])
        info_dict['opr_state'] = eval('0x'+data[34:36])

        return info_dict
    
    def _remt_ack(self):
        """ 桩回复远程开关机操作
        """
        info_dict = {}
        info_dict['pile_code'] = data[0:32]                     # 16位桩运营编码
        info_dict['session_id'] = eval(data[32:64])             # 会话ID
        info_dict['charge_port'] = eval('0x'+data[64:66])       # 充电接口编号
        info_dict['opr_type'] = eval('0x'+data[66:68])          # 操作类型：开机OR关机
        info_dict['opr_state'] = eval('0x'+data[68:70])         # 控制状态：成功OR失败
        info_dict['fail_reason'] = eval('0x'+data[70:72])       # 失败原因

        return info_dict

    def _set_ack(self):
        """ 桩回复更改id
        """
        info_dict = {}
        info_dict['old_code'] = data[0:32]   # 旧桩运营编码
        info_dict['new_code'] =  data[32:64] # 新桩运营编码

        return info_dict

    def _remt_rst(self):
        """ 桩上传远程开关机操作结果
        """
        info_dict = {}
        info_dict['pile_code'] = data[0:32]                     # 16位桩运营编码
        info_dict['session_id'] = eval(data[32:64])             # 会话ID
        info_dict['charge_port'] = eval('0x'+data[64:66])       # 充电接口编号
        info_dict['opr_type'] = eval('0x'+data[66:68])          # 操作类型：开机OR关机
        info_dict['opr_state'] = eval('0x'+data[68:70])         # 控制状态：成功OR失败
        info_dict['fail_reason'] = eval('0x'+data[70:72])       # 失败原因

        return info_dict

    def _do_d2s(self):
        """ 指定字典id转换成字符串
        """
        return self._d2s_func_dict[self._mid]()

    def _do_s2d(self):
        """ 将字符串转换成字典
        """
        if self._msg_check() == False:
            return
        return self._s2d_func_dict[self._mid]()

    # 外部接口
    def set_msg(self,msg,mid=''):
        if type(msg) is str :
            self._msg = msg
            self._state = MSG_S2D
            return True
        elif type(msg) is dict:
            id_list = ['27','29','2B','2D','2F','30','40','42','44','46','49','4A'] 
            if mid not in id_list:
                print 'dict对应id非法'
                return False
            self._msg = msg
            self._mid = mid
            self._state = MSG_D2S
            return True
        else:
            return False
    def get_id(self):
        """ 获取id
        """
        return self._mid
        
    def msg_conv(self):
        """ 消息转换
        """
        if self._state == MSG_S2D:
           return  self._do_s2d()
        elif self._state == MSG_D2S:
           return self._do_d2s()
        else:
            return
            
def main():

    msg = MsgConv(START_ACK_DATA)
    info = {'pile_code':'0000000000123456','user_id':345,'start_state':0,'charge_port':0}
    info1 = {'pile_code':'0000000000123456','time':123}
    msg.set_msg(info,'41')
    print msg.msg_conv()

if __name__ == '__main__':
    main()
 
