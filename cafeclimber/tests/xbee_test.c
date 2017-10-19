#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include <xbee.h>

int main(void) {
    struct xbee *xbee;
    struct xbee_con *con;
    unsigned char txRet;
    xbee_err ret;

    if ((ret = xbee_setup(&xbee, "xbee1", "/dev/ttyUSB0", 57600)) != XBEE_ENONE) {
        printf("ret: %d (%s)\n", ret, xbee_errorToStr(ret));
        return ret;
    }

    if ((ret = xbee_conNew(xbee, &con, "Local AT", NULL)) != XBEE_ENONE) {
        xbee_log(xbee, -1, "xbee_conNew() returned: %d (%s)", ret, xbee_errorToStr(ret));
        return ret;
    }

    ret = xbee_conTx(con, &txRet, "NI");

    printf("tx: %d\n", ret);
    if(ret) {
        printf("txRet: %d\n", txRet);
    } else {
        struct xbee_pkt *pkt;
        if ((ret = xbee_conRx(con, &pkt, NULL)) != XBEE_ENONE) {
            printf("Error after calling xbee_conRx(): %s\n", xbee_errorToStr(ret));
        } else {
            int i;
            printf("Response is %d bytes long:\n", pkt->dataLen);
            for (i = 0; i < pkt->dataLen; i++) {
                unsigned char c = (((pkt->data[i] >= ' ') && (pkt->data[i] <= '~')) ? pkt->data[i] : '.');
                printf("%3d: 0x%02X - %c\n", i, pkt->data[i], c);
            }
        }
    }

    if ((ret = xbee_conEnd(con)) != XBEE_ENONE) {
        xbee_log(xbee, -1, "xbee_conEnd() returned: %d", ret);
        return ret;
    }

    xbee_shutdown(xbee);

    return 0;
}
