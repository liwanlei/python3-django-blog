from email import encoders
from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
import smtplib
def _format_addr(s):
    name, addr = parseaddr(s)
    return formataddr((Header(name, 'utf-8').encode(), addr))
def send_text(to_addr,email,code):
    from_addr='952943386@qq.com'
    password='zjbuavvaffibbdca'

    message =MIMEText( u"""
                <h2>博客(<a  target=_blank>leiziboke.com</a>)<h2><br />
    <table border="1px" cellpadding="3" cellspacing="0">
        <thead></thead>
            <tr bgcolor="#d3d3d3">
                <th>邮箱</th>
                <th>验证码</th>
            </tr>
        <tbody>
            <tr>
                <td>%s</td>
                <td>%s</td>
            </tr>
        </tbody>
    </table>
                <br/><span style="color: red;font-size: medium">请保管好您的验证，有效期10分钟</span>
                """ % (email, code),'html','utf-8')

    message['From'] = _format_addr('博客 <%s>' % from_addr)
    message['To'] = _format_addr('管理员 <%s>' % to_addr)
    message['Subject'] = Header('重置密码', 'utf-8').encode()

    server = smtplib.SMTP_SSL("smtp.qq.com", 465)
    try:
        server.login(from_addr, password)
        server.sendmail(from_addr, [to_addr], message.as_string())
        server.quit()
        return 200
    except:
        pass