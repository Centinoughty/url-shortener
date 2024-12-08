module.exports = (url) => {
  const length = Number(process.env.LENGTH);
  return url.length === length && /^[a-zA-Z0-9]+$/.test(url);
};
