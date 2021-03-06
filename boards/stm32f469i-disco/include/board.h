/*
 * Copyright (C) 2021 luisan00
 *
 * This file is subject to the terms and conditions of the GNU Lesser General
 * Public License v2.1. See the file LICENSE in the top level directory for more
 * details.
 */

/**
 * @ingroup     boards_stm32f469i-disco
 * @{
 *
 * @file
 * @brief       Board specific definitions for the STM32F469I-DISCO board
 *
 * @author      Luis A. Ruiz <luisan00@hotmail.com>
 */
#ifndef BOARD_H
#define BOARD_H

#include "cpu.h"
#include "periph_conf.h"

#ifdef __cplusplus
extern "C"
{
#endif

/**
 * @name Macros for controlling the on-board LEDs
 * @{
 */
#define LED0_PIN GPIO_PIN(PORT_G, 6)
#define LED1_PIN GPIO_PIN(PORT_D, 4)
#define LED2_PIN GPIO_PIN(PORT_D, 5)
#define LED3_PIN GPIO_PIN(PORT_K, 3)

#define LED0_PORT GPIOG
#define LED1_PORT GPIOD
#define LED2_PORT GPIOD
#define LED3_PORT GPIOK

#define LED0_MASK (1 << 6)
#define LED1_MASK (1 << 4)
#define LED2_MASK (1 << 5)
#define LED3_MASK (1 << 3)

#define LED0_ON (LED0_PORT->BSRR = LED0_MASK)
#define LED0_OFF (LED0_PORT->BSRR = (LED0_MASK << 16))
#define LED0_TOGGLE (LED0_PORT->ODR ^= LED0_MASK)

#define LED1_ON (LED1_PORT->BSRR = LED1_MASK)
#define LED1_OFF (LED1_PORT->BSRR = (LED1_MASK << 16))
#define LED1_TOGGLE (LED1_PORT->ODR ^= LED1_MASK)

#define LED2_ON (LED2_PORT->BSRR = LED2_MASK)
#define LED2_OFF (LED2_PORT->BSRR = (LED2_MASK << 16))
#define LED2_TOGGLE (LED2_PORT->ODR ^= LED2_MASK)

#define LED3_ON (LED3_PORT->BSRR = LED3_MASK)
#define LED3_OFF (LED3_PORT->BSRR = (LED3_MASK << 16))
#define LED3_TOGGLE (LED3_PORT->ODR ^= LED3_MASK)
/** @} */

/**
 * @name User button
 * @{
 */
#define BTN0_PIN GPIO_PIN(PORT_A, 0)
#define BTN0_MODE GPIO_IN
/** @} */

#ifdef __cplusplus
}
#endif

#endif /* BOARD_H */
/** @} */
