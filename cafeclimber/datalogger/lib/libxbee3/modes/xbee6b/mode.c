/*
	libxbee - a C library to aid the use of Digi's XBee wireless modules
	          running in API mode.

	Copyright (C) 2009 onwards  Attie Grande (attie@attie.co.uk)

	libxbee is free software: you can redistribute it and/or modify it
	under the terms of the GNU Lesser General Public License as published by
	the Free Software Foundation, either version 3 of the License, or
	(at your option) any later version.

	libxbee is distributed in the hope that it will be useful,
	but WITHOUT ANY WARRANTY; without even the implied warranty of
	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
	GNU Lesser General Public License for more details.

	You should have received a copy of the GNU Lesser General Public License
	along with this program.  If not, see <http://www.gnu.org/licenses/>.
*/

#include <stdio.h>
#include <stdlib.h>
#include <stdarg.h>
#include <string.h>

#include "../../internal.h"
#include "../../xbee_int.h"
#include "../../log.h"
#include "../../mode.h"
#include "../../frame.h"
#include "../../pkt.h"
#include "../common.h"
#include "mode.h"
#include "at.h"
#include "data.h"
#include "io.h"

static xbee_err init(struct xbee *xbee, va_list ap);
static xbee_err mode_shutdown(struct xbee *xbee);

/* ######################################################################### */

static xbee_err init(struct xbee *xbee, va_list ap) {
	xbee_err ret;
	char *t;
	struct xbee_modeData *data;
	
	if (!xbee) return XBEE_EMISSINGPARAM;
	
	if ((data = malloc(sizeof(*data))) == NULL) return XBEE_ENOMEM;
	memset(data, 0, sizeof(*data));
	xbee->modeData = data;
	
	ret = XBEE_ENONE;
	
	/* currently I don't see a better way than this - using va_arg()... which is gross */	
	t = va_arg(ap, char*);
	if ((data->serialInfo.device = malloc(strlen(t) + 1)) == NULL) { ret = XBEE_ENOMEM; goto die; }
	strcpy(data->serialInfo.device, t);
	
	data->serialInfo.baudrate = va_arg(ap, int);
	
	if ((ret = xsys_serialSetup(&data->serialInfo)) != XBEE_ENONE) goto die;
	
	return XBEE_ENONE;
die:
	mode_shutdown(xbee);
	return ret;
}

static xbee_err mode_shutdown(struct xbee *xbee) {
	struct xbee_modeData *data;
	
	if (!xbee) return XBEE_EMISSINGPARAM;
	if (!xbee->mode || !xbee->modeData) return XBEE_EINVAL;
	
	data = xbee->modeData;
	
	xsys_serialShutdown(&data->serialInfo);
	if (data->serialInfo.device) free(data->serialInfo.device);
	if (data->serialInfo.txBuf) free(data->serialInfo.txBuf);
	free(xbee->modeData);
	xbee->modeData = NULL;
	
	return XBEE_ENONE;
}

/* ######################################################################### */

xbee_err xbee_s6b_ip_addressTest(const unsigned char *addr, size_t len) {
	/* never store an updated address... */
	return XBEE_EINVAL;
}

/* ######################################################################### */

xbee_err xbee_s6b_transmitStatus_rx_func(struct xbee *xbee, void *arg, unsigned char identifier, struct xbee_tbuf *buf, struct xbee_frameInfo *frameInfo, struct xbee_conAddress *address, struct xbee_pkt **pkt) {
	struct xbee_pkt *iPkt;
	xbee_err ret;
	
	if (!xbee || !frameInfo || !buf || !address || !pkt) return XBEE_EMISSINGPARAM;
	
	ret = XBEE_ENONE;
	
	if (buf->len != 3) {
		ret = XBEE_ELENGTH;
		goto die1;
	}
	
	frameInfo->active = 1;
	frameInfo->id = buf->data[1];
	frameInfo->retVal = buf->data[2];
	
	if ((ret = xbee_pktAlloc(&iPkt, NULL, 2)) != XBEE_ENONE) return ret;
	
	iPkt->dataLen = 2;
	iPkt->data[0] = buf->data[1];
	iPkt->data[1] = buf->data[2];
	iPkt->data[iPkt->dataLen] = '\0';
	
	*pkt = iPkt;
	
	goto done;
die1:
done:
	return ret;
}

/* ######################################################################### */

struct xbee_modeDataHandlerRx xbee_s6b_transmitStatus_rx  = {
	.identifier = 0x89,
	.func = xbee_s6b_transmitStatus_rx_func,
};
struct xbee_modeConType xbee_s6b_transmitStatus = {
	.name = "Transmit Status",
	.allowFrameId = 1,
	.useTimeout = 0,
	.addressRules = ADDR_NONE,
	.rxHandler = &xbee_s6b_transmitStatus_rx,
	.txHandler = NULL,
};

/* ######################################################################### */

xbee_err xbee_s6b_modemStatus_rx_func(struct xbee *xbee, void *arg, unsigned char identifier, struct xbee_tbuf *buf, struct xbee_frameInfo *frameInfo, struct xbee_conAddress *address, struct xbee_pkt **pkt) {
	struct xbee_pkt *iPkt;
	xbee_err ret;

	if (!xbee || !frameInfo || !buf || !address || !pkt) return XBEE_EMISSINGPARAM;
	
	if (buf->len != 2) return XBEE_ELENGTH;
	
	if ((ret = xbee_pktAlloc(&iPkt, NULL, 1)) != XBEE_ENONE) return ret;
	
	iPkt->dataLen = 1;
	iPkt->data[0] = buf->data[1];
	iPkt->data[iPkt->dataLen] = '\0';
	
	*pkt = iPkt;
	
	return 0;
}

/* ######################################################################### */

struct xbee_modeDataHandlerRx xbee_s6b_modemStatus_rx  = {
	.identifier = 0x8A,
	.func = xbee_s6b_modemStatus_rx_func,
};
struct xbee_modeConType xbee_s6b_modemStatus = {
	.name = "Modem Status",
	.allowFrameId = 0,
	.useTimeout = 0,
	.addressRules = ADDR_NONE,
	.rxHandler = &xbee_s6b_modemStatus_rx,
	.txHandler = NULL,
};

/* ######################################################################### */

xbee_err xbee_s6b_frameError_rx_func(struct xbee *xbee, void *arg, unsigned char identifier, struct xbee_tbuf *buf, struct xbee_frameInfo *frameInfo, struct xbee_conAddress *address, struct xbee_pkt **pkt) {
	struct xbee_pkt *iPkt;
	xbee_err ret;

	if (!xbee || !frameInfo || !buf || !address || !pkt) return XBEE_EMISSINGPARAM;
	
	if (buf->len != 2) return XBEE_ELENGTH;
	
	if ((ret = xbee_pktAlloc(&iPkt, NULL, 1)) != XBEE_ENONE) return ret;
	
	iPkt->dataLen = 1;
#warning TODO - figure out how to use this feedback...
	iPkt->data[0] = buf->data[1];
	iPkt->data[iPkt->dataLen] = '\0';
	
	*pkt = iPkt;
	
	return 0;
}

/* ######################################################################### */

struct xbee_modeDataHandlerRx xbee_s6b_frameError_rx  = {
	.identifier = 0xFE,
	.func = xbee_s6b_frameError_rx_func,
};
struct xbee_modeConType xbee_s6b_frameError = {
	.name = "Frame Error",
	.allowFrameId = 0,
	.useTimeout = 0,
	.addressRules = ADDR_NONE,
	.rxHandler = &xbee_s6b_frameError_rx,
	.txHandler = NULL,
};

/* ######################################################################### */

static const struct xbee_modeConType *conTypes[] = {
	&xbee_s6b_transmitStatus,
	&xbee_s6b_modemStatus,
	&xbee_s6b_frameError,
	&xbee_s6b_localAt,
	&xbee_s6b_remoteAt,
	&xbee_s6b_data,
	&xbee_s6b_io,
	/* these items aren't currently supported by the firmware:
	  File Put
	  Device Request
	  Device Response Status
	*/
	NULL
};

const struct xbee_mode mode_xbee6b = {
	.name = "xbee6b",
	
	.conTypes = conTypes,
	
	.init = init,
	.prepare = NULL,
	.shutdown = mode_shutdown,
	
	.rx_io = xbee_xbeeRxIo,
	.tx_io = xbee_xbeeTxIo,
	
	.thread = NULL,
};
