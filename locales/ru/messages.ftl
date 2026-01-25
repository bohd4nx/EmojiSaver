start-message = 
    {$hello} <b>Привет, {$name}!</b>
    
    Скачивай и конвертируй стикеры и эмодзи Telegram в форматы <code>TGS</code>, <code>JSON</code>, <code>Lottie</code> и <code>PNG</code>.
    
    <b>{$convert} Что я умею:</b> [/help]
    • Извлекать кастомные (премиум) эмодзи из сообщений
    • Конвертировать стикеры в редактируемые форматы
    • Скачивать целые паки стикеров/эмодзи
    
    {$download} <b>Всего скачиваний:</b> {$downloads}
    
    <b>{$search} Быстрый старт:</b> Отправь мне эмодзи, стикер или вставь ссылку на пак!
    
    {$github} <a href="{$github_link}">GitHub</a> • {$telegram} <a href="{$developer}">Разработчик</a>

help-message = 
    {$info} <b>Как использовать:</b>
    
    {$one} <b>Пользовательские эмодзи:</b>
    • Отправь любое сообщение с кастомными (премиум) эмодзи
    • Все эмодзи будут извлечены и конвертированы автоматически
    
    {$two} <b>Стикеры:</b>
    • Отправь или перешли любой стикер
    • Конвертируется в редактируемые форматы (JSON, Lottie, PNG)
    
    {$three} <b>Целые паки:</b>
    • Вставь ссылку на пак: <code>https://t.me/addstickers/PackName</code>
    • Или эмодзи пак: <code>https://t.me/addemoji/PackName</code>
    • Весь пак будет скачан и конвертирован
    
    {$clue} <b>Подсказка:</b> Для обычных статических эмодзи используй:
    <code>https://t.me/addemoji/StaticEmoji</code>
    <code>https://t.me/addstickers/StaticEmoji</code>
    
    {$box} <b>Форматы вывода:</b>
    • <code>.tgs</code> — Оригинальный формат Telegram
    • <code>.json</code> — Несжатая Lottie animation
    • <code>.lottie</code> — Сжатый Lottie (формат LottieFiles)
    • <code>.png</code> — Растровое изображение (первый кадр, 512×512px)

format-warning = 
    {$warning} <b>Уведомление о формате</b>
    
    Некоторые элементы не удалось конвертировать.
    Оригинальные файлы сохранены как есть.

processing-error = 
    {$forbidden} <b>Ошибка:</b>
    
    <code>{$error}</code>
    
    Пожалуйста, попробуйте снова или обратитесь к {$telegram} <a href="{$developer}">разработчику</a>

processing = {$processing} <b>Обрабатываю ваш запрос...</b>

processing-pack = {$processing} <b>Обрабатываю: {$current}/{$total}</b>

processing-failed = 
    {$forbidden} <b>Обработка не удалась</b>
    
    Попробуй позже или обратитесь к {$telegram} <a href="{$developer}">разработчику</a>

pack-not-found = 
    {$forbidden} <b>Пак не найден</b>
    
    Проверь ссылку и попробуй снова.

no-custom-emoji = 
    {$forbidden} <b>Кастомные (премиум) эмодзи не найдены</b>
    
    Отправь сообщение с кастомными эмодзи.

rate-limit-alert = {$forbidden} Пожалуйста, подождите {$seconds} секунд перед отправкой следующего запроса!
