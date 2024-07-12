
# Begin Routine
# 1. Image blank

# 2. Withdraw buffer from inlet
waste_pump.withdraw_rate('200 n/m')
waste_pump.run()

# 3. Infuse cells
cell_pump.run()

# 4. FF withdraw outlet pump
outlet_pump.withdraw_rate('200 n/m')
outlet_pump.run()

# 5. Turn on voltage

# 6. Wait 5 min withdraw outlet pump
outlet_pump.withdraw_rate('50 n/m')
outlet_pump.run()

# 7. Withdraw cells from inlet
waste_pump.withdraw_rate('200 n/m')
waste_pump.run()

# 8. Infuse buffer
buffer_pump.run()

# 9. Wait ~2 min for channel to rinse
outlet_pump.withdraw_rate('50 n/m')
outlet_pump.run()

# 10. Image tips

# 11. Turn off voltage

# 12. Image transfer

# 12. FF withdraw flow pump
outlet_pump.withdraw_rate('200 n/m')
outlet_pump.run()

