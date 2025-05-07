import logging
import time
from urllib.parse import unquote

from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import PlainTextResponse

from app.utils.wechat_util.WXBizMsgCrypt import WXBizMsgCrypt

app = FastAPI()

# 配置参数（需与企业微信后台一致）
sToken = "twH0BWXbuiCIk6LIN"
sEncodingAESKey = "LHEQSfA2Hue6s6ChLLiHx18JS1XD45XtWICY6DfbybC"
sCorpID = "ww4358b0510ad154bc"

# 初始化消息加解密对象
wxcpt = WXBizMsgCrypt(sToken, sEncodingAESKey, sCorpID)


@app.get("/wechat/callback")
async def verify_callback(
    msg_signature: str = Query(..., alias="msg_signature"),
    timestamp: str = Query(..., alias="timestamp"),
    nonce: str = Query(..., alias="nonce"),
    echostr: str = Query(..., alias="echostr"),
):
    """
    企业微信回调验证接口
    文档规范：https://work.weixin.qq.com/api/doc/90000/90135/90930
    """
    try:
        # 1. URL解码（关键步骤）
        decoded_echostr = unquote(echostr)

        # 2. 验证时间戳有效性（防止重放攻击）
        if abs(int(time.time()) - int(timestamp)) > 600:
            logging.error("Timestamp is expired")
            raise HTTPException(status_code=400, detail="Expired timestamp")

        # 3. 执行验证解密
        ret, decrypted_echo = wxcpt.VerifyURL(
            sMsgSignature=msg_signature,
            sTimeStamp=timestamp,
            sNonce=nonce,
            sEchoStr=decoded_echostr,
        )

        # 4. 处理验证结果
        if ret != 0:
            logging.error(f"验证失败，错误码：{ret}")
            raise HTTPException(
                status_code=403, detail=f"Verify failed with code {ret}"
            )
        return PlainTextResponse(
            content=decrypted_echo,
            media_type="text/plain",
            headers={"Content-Disposition": "inline"}
        )

    except Exception as e:
        logging.error("回调验证异常")
        raise HTTPException(status_code=500, detail=str(e))
