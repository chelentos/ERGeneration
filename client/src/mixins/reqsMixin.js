export default {
  methods: {
    // eslint-disable-next-line consistent-return
    translateReqType(req) {
      if (req === 'FT') {
        return 'Отказоучтойчивость'
      } if (req === 'F') {
        return 'Функциональность'
      } if (req === 'LF') {
        return 'UI/UX'
      } if (req === 'SE') {
        return 'Безопасность'
      } if (req === 'SC') {
        return 'Масштабируемость'
      } if (req === 'A') {
        return 'Доступность'
      } if (req === 'O') {
        return 'Эксплуатация'
      } if (req === 'US') {
        return 'Юзабилити'
      } if (req === 'L') {
        return 'Законность'
      } if (req === 'PE') {
        return 'Производительность'
      }
    },
    translateNum(num, mandatory) {
      if (num === 'Sing' && mandatory) {
        return '1'
      } else if (num === 'Sing' && !mandatory) {
        return '0..1'
      } else if (num === 'Plur' && !mandatory) {
        return '0..∞'
      } else if (num === 'Plur' && mandatory) {
        return '1..∞'
      }
    }
  },
}
