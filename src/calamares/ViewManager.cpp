/* === This file is part of Calamares - <http://github.com/calamares> ===
 *
 *   Copyright 2014, Teo Mrnjavac <teo@kde.org>
 *
 *   Calamares is free software: you can redistribute it and/or modify
 *   it under the terms of the GNU General Public License as published by
 *   the Free Software Foundation, either version 3 of the License, or
 *   (at your option) any later version.
 *
 *   Calamares is distributed in the hope that it will be useful,
 *   but WITHOUT ANY WARRANTY; without even the implied warranty of
 *   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
 *   GNU General Public License for more details.
 *
 *   You should have received a copy of the GNU General Public License
 *   along with Calamares. If not, see <http://www.gnu.org/licenses/>.
 */

#include "ViewManager.h"

#include <QBoxLayout>

namespace Calamares
{

ViewManager* ViewManager::s_instance = 0;

ViewManager*
ViewManager::instance()
{
    return s_instance;
}

ViewManager::ViewManager( QObject* parent )
    : QObject( parent )
    , m_widget( new QWidget() )
{
    s_instance = this;
    QBoxLayout* mainLayout = new QVBoxLayout;
    mainLayout->setContentsMargins( 0, 0, 0, 0 );
    m_widget->setContentsMargins( 0, 0, 0, 0 );
    mainLayout->setMargin( 0 );
    mainLayout->setSpacing( 0 );
    m_widget->setLayout( mainLayout );

    m_stack = new QStackedWidget( m_widget );
    m_stack->setContentsMargins( 0, 0, 0, 0 );
    mainLayout->addWidget( m_stack );

    m_back = new QPushButton( tr( "&Back" ), m_widget );
    m_next = new QPushButton( tr( "&Next" ), m_widget );

    QBoxLayout* bottomLayout = new QHBoxLayout;
    mainLayout->addLayout( bottomLayout );
    bottomLayout->addStretch();
    bottomLayout->addWidget( m_back );
    bottomLayout->addWidget( m_next );
}


ViewManager::~ViewManager()
{
    m_widget->deleteLater();
}


QWidget*
ViewManager::widget()
{
    return m_widget;
}


void
ViewManager::addPagePlugin( PagePlugin* plugin )
{

}


void
ViewManager::insertPage( AbstractPage* page )
{

}


void
ViewManager::setNext( AbstractPage* page )
{

}


void
ViewManager::removePage( AbstractPage* page )
{

}


void
ViewManager::next()
{
    Q_ASSERT( 0 );
}


void
ViewManager::back()
{
    Q_ASSERT( 0 );
}

}