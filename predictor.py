import subprocess
import os
import os.path
import shutil
import changeidf

def predict(temp):
	if os.path.exists('energyplus/test'):
		shutil.rmtree('energyplus/test')
	os.makedirs('energyplus/test')
	shutil.copyfile('energyplus/format.idf', 'energyplus/test/format.idf')
	shutil.copyfile('energyplus/USA_CA_San.Francisco.Intl.AP.724940_TMY3.epw', 'energyplus/test/USA_CA_San.Francisco.Intl.AP.724940_TMY3.epw')
	changeidf.change(temp=temp, denomination='D')
	subprocess.call("C:/EnergyPlusV8-1-0/RunEPlus.bat formatted USA_CA_San.Francisco.Intl.AP.724940_TMY3", cwd="energyplus/test")
	return [float(i) for i in changeidf.output(denomination='D')[-1][:12]]

if __name__ == '__main__':
	result = predict()
	print(type(result))
	print(result)
