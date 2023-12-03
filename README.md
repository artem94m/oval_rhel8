# Задание
Информация по уязвимостям для Linux систем обычно поставляется от вендора в
формате OVAL.
В рамках данной части задания необходимо:

### Провести частичный анализ OVAL файла от компании RHEL (https://www.redhat.com/security/data/oval/v2/RHEL8/rhel-8.oval.xml.bz2) на первых 3 уязвимостях (патчах). Определить набор объектов, из которых он строится. Понять основную логику "работы" данного формата. Описать текстом объекты, которые были найдены и для чего они используются. (Не более 2-3 фраз по каждому объекту).
OVAL-файл состоит из нескольких основных разделов:
- `generator` - содержит краткую служебную информацию о самом файле
- `definitions` - определения уязвимостей/патчей:
    - `definition` - определение одной уязвимости/патча:
        - `metadata` - краткое описание, ссылки на базы уязвимостей, дата обнаружения и прочее
        - `criteria` и `criterion` - критерии поиска, которые могут быть вложенными и которые можно комбинировать с помощью операторов **OR** и **AND**; ссылаются на `tests` с помощью **test_ref**
- `tests` - проверки, которые необходимо выполнить, чтобы `criteria` был выполнен:
    - `red-def:object` - объект, который надо проверить; ссылаются на `objects` с помощью **object_ref**
    - `red-def:state` - ожидаемое состояние объекта; ссылаются на `states` с помощью **state_ref**
- `objects` - список объектов
- `states` - список состояний


### В рамках каждого определения уязвимости, есть критерии по ее выявлению: какие из критериев на ваш взгляд лишние?
Сам xml-файл называется `rhel-8.oval.xml`, а значит содержит описания уязвимостей/патчей, характерных только для **RHEL 8**.

В каждом определении есть критерий, который проверяет, что на системе установлен именно RHEL, без привязки к номеру версии:
```xml
<criterion comment="Red Hat Enterprise Linux must be installed" test_ref="oval:com.redhat.rhba:tst:20191992005"/>
```

Помимо этого, в каждом определении есть проверка на то, что на системе установлена конкретная версия ОС (**RHEL 8** или **Red Hat CoreOS 4**):
```xml
<criteria operator="OR">
 <criterion comment="Red Hat Enterprise Linux 8 is installed" test_ref="oval:com.redhat.rhba:tst:20191992003"/>
 <criterion comment="Red Hat CoreOS 4 is installed" test_ref="oval:com.redhat.rhba:tst:20191992004"/>
</criteria>
```

В связи с этим, проверка на тип ОС без привязки к номеру версии является избыточной и может быть удалена.

### Предложить и кратко описать свой вариант по упрощению формата для описания уязвимости вместе с проверками.
#### Вариант A
Если требуется сохранить совместимость с форматом OVAL, то:
- из всех определений можно убрать:
    ```xml
    <criteria operator="OR">
        <criterion comment="Red Hat Enterprise Linux must be installed" test_ref="oval:com.redhat.rhba:tst:20191992005"/>
    ...
    ```
- из тестов убрать:
    ```xml
        <red-def:rpmverifyfile_test check="none satisfy" comment="Red Hat Enterprise Linux must be installed" id="oval:com.redhat.rhba:tst:20191992005" version="635">
            <red-def:object object_ref="oval:com.redhat.rhba:obj:20191992002"/>
            <red-def:state state_ref="oval:com.redhat.rhba:ste:20191992005"/>
        </red-def:rpmverifyfile_test>
    ```
- из стэйтов убрать:
    ```xml
        <red-def:rpmverifyfile_state id="oval:com.redhat.rhba:ste:20191992005" version="635">
            <red-def:name operation="pattern match">^redhat-release</red-def:name>
        </red-def:rpmverifyfile_state>
    ```

#### Вариант B
Если нет необходимости сохранить совместимость с форматом OVAL, то:
- повторить шаги из подпункта A
- создать новый подраздел `<common_criteria>`, куда вынести проверку на конкретную ОС:
    ```xml
        <criteria operator="OR">
            <criterion comment="Red Hat Enterprise Linux 8 is installed" test_ref="oval:com.redhat.rhba:tst:20191992003"/>
            <criterion comment="Red Hat CoreOS 4 is installed" test_ref="oval:com.redhat.rhba:tst:20191992004"/>
        </criteria>
    ```
Проверку из `<common_criteria>` можно будет выполнять единожды, и если она неуспешна, то на проверяемой системе можно не искать уязвимости, определенные в `<definitions>`.


### После выполненного в предыдущей пунктах анализа, необходимо разработать приложение на языке Python, которое произведет разбор (парсинг) OVAL-файла (достаточно сделать только первые 3 и связанными с ними объекты) и преобразует его в упрощенный формат.
Для варианта A был написан скрипт `process_rhel8_oval_compatible.py`.  
Для варианта B был написан скрипт `process_rhel8_oval_noncompatible.py`.

Для запуска обоих скриптов необходим Python 3.9+ и установка дополнительных модулей: `pip install -r requirements.txt`.  
Оба скрипта ожидают, что файл `rhel-8.oval.xml` будет находится в одной с ними директории.

После запуска скрипта `python process_rhel8_oval_compatible.py` появится файл с результатом `rhel-8.oval_processed_oval_compatible.xml` в той же директории.  
После запуска скрипта `python process_rhel8_oval_noncompatible.py` появится файл с результатом `rhel-8.oval_processed_oval_noncompatible.xml` в той же директории.
