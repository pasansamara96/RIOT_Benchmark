#!/usr/bin/env python3

# Copyright (C) 2020 Inria
#
# This file is subject to the terms and conditions of the GNU Lesser
# General Public License v2.1. See the file LICENSE in the top level
# directory for more details.

"""Generate a header with the number of IRQs for a given STM32 family."""

import os
import argparse
import re


CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
RIOTBASE = os.getenv(
    "RIOTBASE", os.path.abspath(os.path.join(CURRENT_DIR, "../../../..")))
STM32_INCLUDE_DIR = os.path.join(RIOTBASE, "cpu/stm32/include")
STM32_IRQS_DIR = os.path.join(
    RIOTBASE, STM32_INCLUDE_DIR, "irqs/{}/irqs.h")

IRQS_FORMAT = """
/*
 * PLEASE DON'T EDIT
 *
 * This file was automatically generated by
 * ./cpu/stm32/dist/irqs/gen_irqs.py
 */

#ifndef IRQS_{cpu_fam}_H
#define IRQS_{cpu_fam}_H

#ifdef __cplusplus
extern "C" {{
#endif

{irq_lines}

#ifdef __cplusplus
}}
#endif

#endif /* IRQS_{cpu_fam}_IRQ_H */
"""


def list_cpu_lines(cmsis_dir, cpu_fam):
    """Returns the list CPU lines for a given family"""
    headers = os.listdir(cmsis_dir)
    if "Templates" in headers:
        headers.remove("Templates")
    if "partition_stm32l5xx.h" in headers:
        headers.remove("partition_stm32l5xx.h")
    if "partition_stm32u5xx.h" in headers:
        headers.remove("partition_stm32u5xx.h")
    headers.remove("stm32{}xx.h".format(cpu_fam))
    headers.remove("system_stm32{}xx.h".format(cpu_fam))
    return sorted([header.split(".")[0] for header in headers])


def irq_numof(cmsis_dir, cpu_line):
    """Parse the CMSIS to get the list IRQs."""
    cpu_line_cmsis = os.path.join(cmsis_dir, "{}.h".format(cpu_line))

    with open(cpu_line_cmsis, 'rb') as cmsis:
        cmsis_content = cmsis.readlines()

    for line_idx, line in enumerate(cmsis_content):
        try:
            line = line.decode()
        except UnicodeDecodeError:
            # skip line that contains non unicode characters
            continue
        # skip useless lines
        if (
            # Skip lines with comments
            line.startswith("/*") or
            # Skip line starting with too many spaces
            line.startswith(" " * 8) or
            # Skip remapped USB interrupt
            # (set as alias for USBWakeUp_IRQn on stm32f3)
            "USBWakeUp_RMP_IRQn" in line
        ):
            continue
        # Stop at the end of the IRQn_Type enum definition
        if "IRQn_Type" in line \
                and "#else" not in cmsis_content[line_idx + 1].decode():
            break

    # Ensure we are on a valid line, otherwise search in earlier lines
    last_irq_line = cmsis_content[line_idx - 1].decode()
    while last_irq_line.startswith(" " * 8):
        line_idx -= 1
        last_irq_line = cmsis_content[line_idx - 1].decode()

    # Use a regexp to find the last IRQ line index
    irq_numof_match = re.search(r"(= \d+)", last_irq_line).group(0)

    return int(irq_numof_match.replace("= ", "").strip()) + 1


def generate_irqs(context):
    """Use irqs template to generate the irqs.h file."""
    irq_line_first_format = (
        "#if defined({line})\n"
        "#define CPU_IRQ_NUMOF                   ({irq_numof}U)"
    )
    irq_line_format = (
        "#elif defined({line})\n"
        "#define CPU_IRQ_NUMOF                   ({irq_numof}U)")
    irq_lines = []
    for idx, line in enumerate(context["cpu_lines"]):
        if idx == 0:
            irq_lines.append(
                irq_line_first_format.format(**line))
        else:
            irq_lines.append(
                irq_line_format.format(**line))
    irq_lines.append("#endif")

    irqs_content = IRQS_FORMAT.format(
        cpu_fam=context["cpu_fam"].upper(),
        irq_lines="\n".join(irq_lines),
        )
    dest_file = os.path.join(STM32_IRQS_DIR.format(context["cpu_fam"]))

    if not os.path.exists(os.path.dirname(dest_file)):
        os.makedirs(os.path.dirname(dest_file))
    with open(dest_file, "w") as f_dest:
        f_dest.write(irqs_content)


def main(args):
    """Main function."""
    cpu_lines = list_cpu_lines(args.cmsis_dir, args.cpu_fam)
    context = {
        "cpu_fam": args.cpu_fam,
        "cpu_lines": [
            {
                "line": cpu_line.upper().replace("X", "x"),
                "irq_numof": irq_numof(args.cmsis_dir, cpu_line),
            }
            for cpu_line in cpu_lines
        ]
    }
    generate_irqs(context)


PARSER = argparse.ArgumentParser()
PARSER.add_argument("cmsis_dir", help="CMSIS directory")
PARSER.add_argument("cpu_fam", help="STM32 CPU Family")

if __name__ == "__main__":
    main(PARSER.parse_args())
