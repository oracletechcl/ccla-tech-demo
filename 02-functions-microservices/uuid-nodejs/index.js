const { v4: uuidv4 } = require('uuid');

module.exports = async function (context, data) {
  try {
    const stress_ms = data.stress_ms || 0;
    await new Promise(resolve => setTimeout(resolve, stress_ms));
    return {
      uuid: uuidv4(),
      timestamp: new Date().toISOString()
    };
  } catch (e) {
    return { error: e.message };
  }
}
